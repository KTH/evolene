__author__ = 'tinglev@kth.se'

import logging

from modules.util import docker
from modules.util import process
from modules.util import environment
from modules.util import pipeline_data
from modules.util import file_util
from modules.util.exceptions import PipelineException
from modules.util import slack

log = logging.getLogger(__name__)

PACKAGE_JSON = '/package.json'
IMAGE_NAME = 'kthse/npm-package-available'

def run(data):

    if not file_util.is_file(PACKAGE_JSON):
        log.info('No file named "%s" found. No dependencies check will be done.', PACKAGE_JSON)
        return data

    prepare()

    check(data)

    return data

def prepare():
    pull_image_if_missing()

def check(data):
    ncu_output = check_dependencies()
    if ncu_output:
        process_output(ncu_output, data)
    else:
        log.info('Got no output from dep checker.')

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

def process_output(ncu_output, data):

    # The ncu package checker itself needs an upgrade. Skip informing. Pls upgarde the docker image.
    if "Update available" in ncu_output:
        return

    # No deps in package.json
    if "No dependencies" in ncu_output:
        return

    # All is dandy
    if "All dependencies match the latest package" in ncu_output:
        return

    log_and_slack(clean(ncu_output), data)

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
    upgrades_information = upgrades_information.replace('  ', ' ')
    upgrades_information = upgrades_information.replace('\n', '')

    return upgrades_information

def log_and_slack(upgrades_information, data):
    log.info('New dependencies version(s) available: \n %s', upgrades_information)

    if environment.use_experimental():
        msg = (f'*{data[pipeline_data.IMAGE_NAME]}* <https://www.npmjs.com/package/npm-check-updates|NPM Check Updates> reported new version(s) available. ``` {upgrades_information} ``` Run `ncu -u` in the root of your project to update.')
        slack.send_to_slack(msg, icon=':jenkins:')

def check_dependencies():
    image_name = IMAGE_NAME
    cmd = f'docker run --tty --rm -v ${{WORKSPACE}}/package.json:/package.json {image_name}'
    try:
        return process.run_with_output(cmd)
    except PipelineException as pipeline_ex:
        log.warning('Could not check dependencies: "%s"', str(pipeline_ex))
        return None
