__author__ = 'tinglev'

import os
import datetime
import time

IMAGE_NAME = 'IMAGE_NAME'
PROJECT_ROOT = 'WORKSPACE'
GIT_COMMIT = 'GIT_COMMIT'
GIT_BRANCH = 'GIT_BRANCH'
GIT_COMMITTER_NAME = 'GIT_COMMITTER_NAME'
BUILD_NUMBER = 'BUILD_NUMBER'
BUILD_URL = 'BUILD_URL'
BUILD_INFORMATION_OUTPUT_FILE = 'BUILD_INFORMATION_OUTPUT_FILE'
SLACK_WEB_HOOK = 'EVOLENE_SLACK_WEB_HOOK'
SLACK_CHANNELS = 'SLACK_CHANNELS'
REGISTRY_HOST = 'REGISTRY_HOST'
REGISTRY_USER = 'REGISTRY_USER'
REGISTRY_PASSWORD = 'REGISTRY_PASSWORD'
EVOLENE_DIRECTORY = 'EVOLENE_DIRECTORY'
EXPERIMENTAL = 'EXPERIMENTAL'
SKIP_DRY_RUN = 'SKIP_DRY_RUN'
PUSH_PUBLIC = 'PUSH_PUBLIC'
PUSH_AZURE = 'PUSH_AZURE'
AZURE_REGISTRY_HOST = 'AZURE_REGISTRY_HOST'
AZURE_REGISTRY_USER = 'AZURE_REGISTRY_USER'
AZURE_REGISTRY_PASSWORD = 'AZURE_REGISTRY_PASSWORD'
NPM_USER = 'NPM_USER'
NPM_PASSWORD = 'NPM_PASSWORD'
NPM_EMAIL = 'NPM_EMAIL'
DOCKER_BUILD_ARG = 'DOCKER_BUILD_ARG'

def get_npm_email():
    return os.environ.get(NPM_EMAIL)

def get_npm_user():
    return os.environ.get(NPM_USER)

def get_npm_password():
    return os.environ.get(NPM_PASSWORD)

def get_registry_host():
    if get_push_public():
        return "docker.io/kthse"
    if get_push_azure():
        return os.environ.get(AZURE_REGISTRY_HOST)
    return os.environ.get(REGISTRY_HOST)

def get_registry_user():
    if get_push_azure():
        return os.environ.get(AZURE_REGISTRY_USER)
    return os.environ.get(REGISTRY_USER)

def get_registry_password():
    if get_push_azure():
        return os.environ.get(AZURE_REGISTRY_PASSWORD)
    return os.environ.get(REGISTRY_PASSWORD)

def get_image_name():
    return os.environ.get(IMAGE_NAME)

def get_git_commit():
    return os.environ.get(GIT_COMMIT)

def get_git_branch():
    return os.environ.get(GIT_BRANCH)

def get_git_commiter_name():
    return os.environ.get(GIT_COMMITTER_NAME)

def get_project_root():
    return os.environ.get(PROJECT_ROOT)

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

def get_experimental():
    return is_true(EXPERIMENTAL)

def use_dry_run():
    if is_true(SKIP_DRY_RUN):
        return False
    return True

def get_build_url():
    return os.environ.get(BUILD_URL)

def is_true(env_key):
    value = os.environ.get(env_key)
    if value is None:
        return False
    return value.lower() in ['true', 'yes', 'y']

def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def get_docker_build_arg():
    return os.environ.get(DOCKER_BUILD_ARG)
