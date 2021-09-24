__author__ = 'paddy@kth.se'

import logging
import requests
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util import environment, pipeline_data

STATUS_OK = 'OK'
STATUS_ERROR = 'ERROR'
STATUS_NA = 'NA'
STATUS_MISSING = 'MISSING'
STATUS_CI_PLATTFORM_GITHUB: 'Evolene Github'

log = logging.getLogger("-")

def post(data, step, step_value):
    log.info(f'Adding {step} with value {step_value} to ci-status dashboard.')
    base_url = environment.get_ci_status_api_base_url()
    if base_url is None:
        return
    if not base_url.endswith('/'):
        base_url += '/'
    app_name = data[pipeline_data.IMAGE_NAME]
    app_version = data[pipeline_data.IMAGE_VERSION]
    final_url = f'{base_url}evolene/{app_name}/{app_version}/{step}/{step_value}'
    try:
        
        requests.post(final_url)
    except HTTPError as http_ex:
        log.error('ci-status endpoint threw HTTPError with response "%s"', http_ex.response)
    except ConnectTimeout as timeout:
        log.error('Timeout while trying to post to ci-status endpoint: "%s"', timeout)
    except RequestException as req_ex:
        log.error('Exception when trying to post to ci-status endpoint: "%s"', req_ex)

def post_unit_tests_run(data, step_status):
    post(data, 'UNIT_TESTS', step_status)

def post_integration_tests_run(data, step_status):
    post(data, 'INTEGRATION_TESTS', step_status)

def post_platform_validation_run(data, step_status):
    post(data, 'PLATFORM_VALIDATION', step_status)

def post_docker_public_run(data, step_status):
    post(data, 'DOCKER_PUBLIC', step_status)

def post_docker_private_run(data, step_status):
    post(data, 'DOCKER_PRIVATE', step_status)

def post_ci_environment_run(data, step_status):
    post(data, 'CI_ENVIRONMENT', step_status)

def post_repo_security_scan_run(data, step_status):
    post(data, 'REPO_SECURITY_SCAN', step_status)
