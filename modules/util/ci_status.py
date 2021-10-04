__author__ = 'paddy@kth.se'

import logging
import requests
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util import environment, pipeline_data

STATUS_OK = 'OK'
STATUS_ERROR = 'ERROR'
STATUS_NA = 'NA'
STATUS_MISSING = 'MISSING'
STATUS_CI_PLATTFORM_GITHUB = 'Evolene Github'

log = logging.getLogger("-")

def post(data, step, step_value, severity):
    log.info(f'Adding {step} with value {step_value} to ci-status dashboard.')
    base_url = environment.get_ci_status_api_base_url()
    if base_url is None:
        return
    if not base_url.endswith('/'):
        base_url += '/'
    post_json = create_post_json(data, step, step_value, severity)
    try:
        requests.post(base_url, json=post_json)
    except HTTPError as http_ex:
        log.error('ci-status endpoint threw HTTPError with response "%s"', http_ex.response)
    except ConnectTimeout as timeout:
        log.error('Timeout while trying to post to ci-status endpoint: "%s"', timeout)
    except RequestException as req_ex:
        log.error('Exception when trying to post to ci-status endpoint: "%s"', req_ex)

def create_post_json(data, step, step_value, severity):
    return {
        'reportingService': 'evolene',
        'serviceName': data[pipeline_data.IMAGE_NAME],
        'serviceVersion': data[pipeline_data.IMAGE_VERSION],
        'stepName': step,
        'stepStatus': step_value,
        'severity': severity
    }

def post_unit_tests_run(data, step_status, severity):
    post(data, 'UNIT_TESTS', step_status, severity)

def post_integration_tests_run(data, step_status, severity):
    post(data, 'INTEGRATION_TESTS', step_status, severity)

def post_platform_validation_run(data, step_status, severity):
    post(data, 'PLATFORM_VALIDATION', step_status, severity)

def post_docker_public_run(data, step_status, severity):
    post(data, 'DOCKER_PUBLIC', step_status, severity)

def post_docker_private_run(data, step_status, severity):
    post(data, 'DOCKER_PRIVATE', step_status, severity)

def post_ci_environment_run(data, step_status, severity):
    post(data, 'CI_ENVIRONMENT', step_status, severity)

def post_repo_security_scan_run(data, step_status, severity):
    post(data, 'REPO_SECURITY_SCAN', step_status, severity)
