__author__ = 'tinglev'

import os
import datetime
import time

IMAGE_NAME = 'IMAGE_NAME'
PROJECT_ROOT = 'WORKSPACE'
GIT_COMMIT = 'GIT_COMMIT'
GIT_BRANCH = 'GIT_BRANCH'
GIT_COMMITTER_NAME = 'GIT_COMMITTER_NAME'
GIT_URL = 'GIT_URL'
GITHUB_WORKSPACE = 'GITHUB_WORKSPACE'
GITHUB_REPOSITORY = 'GITHUB_REPOSITORY'
GITHUB_RUN_ID = 'GITHUB_RUN_ID'
BUILD_NUMBER = 'BUILD_NUMBER'
BUILD_URL = 'BUILD_URL'
BUILD_INFORMATION_OUTPUT_FILE = 'BUILD_INFORMATION_OUTPUT_FILE'
HOME = 'HOME'
SLACK_WEB_HOOK = 'EVOLENE_SLACK_WEB_HOOK'
SLACK_CHANNELS = 'SLACK_CHANNELS'

REGISTRY_HOST = 'REGISTRY_HOST'
REGISTRY_USER = 'REGISTRY_USER'
REGISTRY_PASSWORD = 'REGISTRY_PASSWORD'

PUBLIC_REGISTRY_HOST = 'PUBLIC_REGISTRY_HOST'
PUBLIC_REGISTRY_USER = 'PUBLIC_REGISTRY_USER'
PUBLIC_REGISTRY_PASSWORD = 'PUBLIC_REGISTRY_PASSWORD'

AZURE_REGISTRY_HOST = 'AZURE_REGISTRY_HOST'
AZURE_REGISTRY_USER = 'AZURE_REGISTRY_USER'
AZURE_REGISTRY_PASSWORD = 'AZURE_REGISTRY_PASSWORD'

EVOLENE_DIRECTORY = 'EVOLENE_DIRECTORY'
EVOLENE_TEST_SECRETS = 'EVOLENE_TEST_SECRETS'
EXPERIMENTAL = 'EXPERIMENTAL'
SKIP_DRY_RUN = 'SKIP_DRY_RUN'
PUSH_PUBLIC = 'PUSH_PUBLIC'
PUSH_AZURE = 'PUSH_AZURE'
BRANCHES_SAVE_STARTING_WITH = 'BRANCHES_SAVE_STARTING_WITH'
BRANCHES_TAG_AS_MAIN = 'BRANCHES_TAG_AS_MAIN'
NPM_USER = 'NPM_USER'
NPM_PASSWORD = 'NPM_PASSWORD'
NPM_EMAIL = 'NPM_EMAIL'
NPM_UPDATES_AVAILABLE = 'NPM_UPDATES_AVAILABLE'
DOCKER_BUILD_ARGS = 'DOCKER_BUILD_ARGS'
SLIM = 'SLIM'
SLIM_ENV = 'SLIM_ENV'

def get_slim():
    return os.environ.get(SLIM)

def get_slim_env():
    return os.environ.get(SLIM_ENV)

def get_npm_email():
    return os.environ.get(NPM_EMAIL)

def get_npm_user():
    return os.environ.get(NPM_USER)

def get_npm_password():
    return os.environ.get(NPM_PASSWORD)

def get_registry_host():
    return os.environ.get(REGISTRY_HOST)

def get_registry_user():
    return os.environ.get(REGISTRY_USER)

def get_registry_password():
    return os.environ.get(REGISTRY_PASSWORD)

def get_public_registry_host():
    return os.environ.get(PUBLIC_REGISTRY_HOST)

def get_public_registry_user():
    return os.environ.get(PUBLIC_REGISTRY_USER)

def get_public_registry_password():
    return os.environ.get(PUBLIC_REGISTRY_PASSWORD)

def get_public_registry_host():
    return "docker.io/kthse"


def get_azure_registry_host():
    return os.environ.get(AZURE_REGISTRY_HOST)

def get_azure_registry_user():
    return os.environ.get(AZURE_REGISTRY_USER)

def get_azure_registry_password():
    return os.environ.get(AZURE_REGISTRY_PASSWORD)

def get_image_name():
    return os.environ.get(IMAGE_NAME)

def get_git_commit():
    return os.environ.get(GIT_COMMIT)

def get_git_url():
    return os.environ.get(GIT_URL)
def get_git_branch():
    return os.environ.get(GIT_BRANCH)

def get_git_commiter_name():
    return os.environ.get(GIT_COMMITTER_NAME)

def get_project_root():
    return os.environ.get(PROJECT_ROOT)

def get_github_workspace():
    return os.environ.get(GITHUB_WORKSPACE)

def get_docker_mount_root():
    if get_github_workspace():
        return get_github_workspace()
    return get_project_root().rstrip('/')

def is_run_inside_docker():
    return get_github_workspace()
    

def get_build_number():
    return os.environ.get(BUILD_NUMBER)

def get_build_information_output_file():
    return os.environ.get(BUILD_INFORMATION_OUTPUT_FILE)

def get_slack_channels():
    channels = os.environ.get(SLACK_CHANNELS)
    if channels:
        return [channel.rstrip() for channel in channels.split(',')]
    return []

def get_slack_web_hook():
    return os.environ.get(SLACK_WEB_HOOK)

def get_evolene_directory():
    return os.environ.get(EVOLENE_DIRECTORY)

def get_push_public():
    return is_true(PUSH_PUBLIC)

def get_push_azure():
    return is_true(PUSH_AZURE)

def get_branches_save_starting_with():
    return os.environ.get(BRANCHES_SAVE_STARTING_WITH)

def get_branches_tag_as_main():
    return is_true(BRANCHES_TAG_AS_MAIN)

def use_dry_run():
    if is_true(SKIP_DRY_RUN):
        return False
    return True

def use_experimental():
    return is_true(EXPERIMENTAL)

def use_update_available():
    '''
    Inform users that there are update available
    for packages in package.json
    '''
    return is_true(NPM_UPDATES_AVAILABLE)

def get_build_url():
    return os.environ.get(BUILD_URL)

def get_home():
    return os.environ.get("HOME")

def get_github_run_id():
    return os.environ.get(GITHUB_RUN_ID)

def get_github_repository():
    return os.environ.get(GITHUB_REPOSITORY)

def get_console_url():
    # https://github.com/KTH/docker-generate-npm-authtoken/actions/runs/897291507
    return f'https://github.com/{get_github_repository()}/actions/runs/{get_github_run_id()}'

def is_true(env_key):
    return is_true_value(os.environ.get(env_key))

def is_true_value(value, true_values=[ "yes", "true" ]):
    if value is None:
        return False
    
    if true_values is None:
        return False
        
    if value.lower() in true_values:
        return True

    return False

def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def get_tests_secrets():
    secrets = os.environ.get(EVOLENE_TEST_SECRETS)
    print(secrets)
    if secrets:
        return secrets.replace('\n', ' ')
    return ""

def get_docker_build_args():
    args = os.environ.get(DOCKER_BUILD_ARGS)
    if args:
        return [args.rstrip() for args in args.split(',')]
    return []

def get_env_with_default_value(name, default_value):
    value = os.environ.get(name)
    if not value:
        return default_value
    return value.strip()