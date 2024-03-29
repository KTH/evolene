__author__ = 'tinglev'

from os import environ
import re
from modules.util import process
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import pipeline_data
from modules.util import file_util
import logging


log = logging.getLogger("-")


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
    output = process.run_with_output('docker images')
    return grep(image_id, output)


def get_container_status(container_id):
    return process.run_with_output(f'docker inspect --format=\'{{{{.State.Status}}}}\' '
                                   f'{container_id}', check=True).replace('\n', '')


def run(image_id):
    return process.run_with_output(f'docker run -d {image_id}').rstrip()


def get_image_id(tag):
    return process.run_with_output(
        f'docker image ls --filter reference="{tag}" -q'
    ).rstrip()


def stop_and_remove_container(container_id):
    return process.run_with_output(f'docker rm -f {container_id}', check=True)


def tag_image(image_id, tag):
    return process.run_with_output(f'docker tag {image_id} {tag}')


def push(registry_image_name):
    return process.run_with_output(f'docker push {registry_image_name}', log_cmd=True, check=True)


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
    

def login_azure():
    return login(environment.get_azure_registry_user(), environment.AZURE_REGISTRY_PASSWORD, environment.get_azure_registry_host())


def login_public():
    return login(environment.get_public_registry_user(), environment.PUBLIC_REGISTRY_PASSWORD)


def login_github():
    return login(environment.get_github_registry_user(), environment.GITHUB_REGISTRY_PASSWORD, environment.get_github_registry_host())


def login(user, pwd_env, host=""):
    # Send password via standard in.
    retval = process.run_with_output(
        f'echo ${pwd_env} | docker login --username {user} --password-stdin {host}')
    return retval


def run_test(compose_test_file, data):
    image_id = data[pipeline_data.LOCAL_IMAGE_ID]
    cmd = (f'cd {file_util.get_project_root()} && '
           f'{environment.get_tests_secrets_export_cmd()} LOCAL_IMAGE_ID={image_id}  WORKSPACE={environment.get_docker_mount_root()} docker-compose --file {compose_test_file} up '
           f'--build '
           f'--no-log-prefix '
           f'--quiet-pull '
           f'--abort-on-container-exit '
           f'--always-recreate-deps '
           f'--force-recreate')

    output = process.run_with_output(cmd, log_cmd=True, check=True)

    cmd_clean = (f'docker-compose --file {compose_test_file} down -v')

    process.run_with_output(cmd_clean)

    return output


def grep(pattern, string):
    regex = r'^.*('+pattern+r').*$'
    for line in string.split('\n'):
        match = re.search(regex, line)
        if match:
            return match.group(0)
    return None
