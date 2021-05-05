__author__ = 'tinglev'

from os import environ
from modules.util import process
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import pipeline_data
from modules.util import file_util
import logging


log = logging.getLogger(__name__)

def build(labels=None, build_args=None):
    flags = '--pull'
    #build_local_image_id = 'docker build --quiet --pull'
    root = environment.get_project_root()
    if labels:
        for label in labels:
            flags = f'{flags} --label {label}'
    if build_args:
        for arg in build_args:
            flags = f'{flags} --build-arg {arg}'
    
    # Build 
    log.info(process.run_with_output(f'docker build {flags} {root}'))
    
    # Rerun build to get a local image id.
    return process.run_with_output(f'docker build --quiet {flags} {root}')

def grep_image_id(image_id):
    try:
        return process.run_with_output(f'docker images | grep {image_id}')
    except PipelineException:
        # An exception here means that the grep failed and that the image is missing
        return None

def get_container_status(container_id):
    return process.run_with_output(f'docker inspect --format=\'{{{{.State.Status}}}}\' '
                                   f'{container_id}').replace('\n', '')

def run(image_id):
    return process.run_with_output(f'docker run -d {image_id}').rstrip()

def get_image_id(tag):
    return process.run_with_output(
        f'docker image ls --filter reference="{tag}" -q'
    ).rstrip()

def stop_and_remove_container(container_id):
    return process.run_with_output(f'docker rm -f {container_id}')

def tag_image(image_id, tag):
    return process.run_with_output(f'docker tag {image_id} {tag}')

def push(registry_image_name):
    return process.run_with_output(f'docker push {registry_image_name}')

def inspect_image(image_id):
    return process.run_with_output(f'docker image inspect {image_id}')

def pull(image_name):
    return process.run_with_output(f'docker pull {image_name}')

def run_unit_test_compose(compose_test_file, data):
    return run_test(compose_test_file, data)

def run_integration_tests(compose_test_file, data):
    return run_test(compose_test_file, data)

def run_dry_run_compose(compose_test_file, data):
    return run_test(compose_test_file, data)

def login():
    host = environment.get_registry_host()
    user = environment.get_registry_user()
    pwd = environment.get_registry_password()
    retval = process.run_with_output(f'docker login -u {user} -p {pwd} {host}', False)
    return retval

def login_azure():
    host = environment.get_azure_registry_host()
    user = environment.get_azure_registry_user()
    pwd = environment.get_azure_registry_password()
    retval = process.run_with_output(f'docker login -u {user} -p {pwd} {host}', False)
    return retval

def run_test(compose_test_file, data):
    image_id = data[pipeline_data.LOCAL_IMAGE_ID]
    cmd_test = (f'cd {file_util.get_project_root()} && LOCAL_IMAGE_ID={image_id} '
           f'{environment.get_tests_secrets()} T=A docker-compose --file {compose_test_file} up '
           f'--build '
           f'--abort-on-container-exit '
           f'--always-recreate-deps '
           f'--force-recreate')

    output = process.run_with_output(cmd_test)

    cmd_clean = (f'docker-compose --file {compose_test_file} down -v')

    process.run_with_output(cmd_clean)

    return output
