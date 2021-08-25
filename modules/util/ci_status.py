__author__ = 'paddy@kth.se'

import requests
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util import environment, log

STATUS_OK = 'OK'
STATUS_ERROR = 'ERROR'
STATUS_NA = 'NA'
STATUS_MISSING = 'MISSING'

def post(app_name, step, step_value):
    base_url = environment.get_ci_status_api_base_url()
    if base_url is None:
        return
    if not base_url.endswith('/'):
        base_url += '/'
    final_url = f'{base_url}evolene/{app_name}/{step}/{step_value}'
    try:
        requests.post(final_url)
    except HTTPError as http_ex:
        log.error('ci-status endpoint threw HTTPError with response "%s"', http_ex.response)
    except ConnectTimeout as timeout:
        log.error('Timeout while trying to post to ci-status endpoint: "%s"', timeout)
    except RequestException as req_ex:
        log.error('Exception when trying to post to ci-status endpoint: "%s"', req_ex)
    
def post_unit_tests_run(app_name, step_status):
    post(app_name, 'UNIT_TESTS', step_status)

def post_integration_tests_run(app_name, step_status):
    post(app_name, 'INTEGRATION_TESTS', step_status)

def post_platform_validation_run(app_name, step_status):
    post(app_name, 'PLATFORM_VALIDATION', step_status)

def post_docker_public_run(app_name, step_status):
    post(app_name, 'DOCKER_PUBLIC', step_status)

def post_docker_private_run(app_name, step_status):
    post(app_name, 'DOCKER_PRIVATE', step_status)

