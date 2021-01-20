__author__ = 'tinglev@kth.se'

import logging

from modules.util import docker
from modules.util import process
from modules.util import environment
from modules.util import file_util
from modules.util.exceptions import PipelineException
from modules.util import slack

log = logging.getLogger(__name__)

PACKAGE_JSON = '/package.json'
IMAGE_NAME = 'kthse/npm-package-available'

def run(name):

    if file_util.is_file(PACKAGE_JSON):
        prepare()
        check(name)
    else:
        log.info('No file named "%s" found. No dependencies check will be done.', PACKAGE_JSON)



def prepare():
    pull_image_if_missing()

def check(name):
    ncu_output = check_dependencies()
    if ncu_output:
        process_output(ncu_output, name)
    else:
        log.debug('Got no output from dep checker.')

def pull_image_if_missing():
    image_grep_output = None
    try:
        image_grep_output = docker.grep_image_id(IMAGE_NAME)

        if not image_grep_output or IMAGE_NAME not in image_grep_output:
            pull_image()

    except PipelineException:
        pull_image()

def pull_image():
    log.debug('Couldnt find local image "%s". Pulling from docker.io.', IMAGE_NAME)
    docker.pull(IMAGE_NAME)

def process_output(ncu_output, name):

    # The ncu package checker itself needs an upgrade. Skip informing. Pls upgarde the docker image.
    if "Update available" in ncu_output:
        return

    # No deps in package.json
    if "No dependencies" in ncu_output:
        return

    # All is dandy
    if "All dependencies match the latest package" in ncu_output:
        return

    log_and_slack(clean(ncu_output), name)

def clean(cmd_output):
    '''
    Checking /package.json
    [] 0/13 0%[] 1/13 7%[] 3/13 23%[] 6/13 46%[] 61%[] 69%[] 11/13 84%[] 12/13 92%[] 13/13 100%
    mocha  ^8.2.0  →  ^8.2.1

    Run  ncu -u  in the root of your project to update
    '''
    index_progressbar_end = cmd_output.index("100%") + len("100%")
    upgrades_information = cmd_output[index_progressbar_end:]

    index_upgrade_info_start = upgrades_information.index("Run")
    upgrades_information = upgrades_information[:index_upgrade_info_start]
    upgrades_information = upgrades_information.replace('            ', '')
    upgrades_information = upgrades_information.replace('\n\n', '')
    upgrades_information = upgrades_information.replace('\n', '')
    upgrades_information = upgrades_information.replace('  ', ' ')
    return upgrades_information.strip()

def log_and_slack(upgrades_information, name):
    log.info('New dependencies version(s) available: \n %s', upgrades_information)

    if environment.use_experimental():
        text = (f'*{name}* <https://www.npmjs.com/package/npm-check-updates|npm check updates> reported new version(s) available. Run `ncu -u` in the root of your project to update.')
        slack.send(text, snippet=upgrades_information, icon=':jenkins:')

def check_dependencies():
    image_name = IMAGE_NAME
    cmd = f'docker run --tty --rm -v ${{WORKSPACE}}/package.json:/package.json {image_name}'
    try:
        return process.run_with_output(cmd)
    except PipelineException as pipeline_ex:
        log.warning('Could not check dependencies: "%s"', str(pipeline_ex))
        return None
