__author__ = 'paddy@kth.se'

import logging
import requests
from modules.util import artifact
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util import environment, pipeline_data

STATUS_OK = 'Ok'
STATUS_ERROR = 'Error'
STATUS_NA = 'N/A'
STATUS_MISSING = 'Missing'
STATUS_CI_PLATTFORM_GITHUB = 'Evolene CI - Github'

log = logging.getLogger("-")

def post(data, step, step_value, severity, description = None):

    if not artifact.should_store():
        log.debug(f'No information about this build will be sent to ci-status.')
        return

    log.info(f'Adding {step} with value {step_value} to ci-status dashboard.')
    url_to_call = create_secure_url()
    headers = create_headers()
    post_json = create_post_json(data, step, step_value, severity, description)
    try:
        requests.post(url_to_call, json=post_json, headers=headers)
    except HTTPError as http_ex:
        log.error('ci-status endpoint threw HTTPError with response "%s"', http_ex.response)
    except ConnectTimeout as timeout:
        log.error('Timeout while trying to post to ci-status endpoint: "%s"', timeout)
    except RequestException as req_ex:
        log.error('Exception when trying to post to ci-status endpoint: "%s"', req_ex)

def create_headers():
    token = environment.get_ci_status_header_token()
    return {'ci-status-token': token}

def create_secure_url():
    base_url = environment.get_ci_status_api_base_url()
    if base_url is None:
        return
    if not base_url.endswith('/'):
        base_url += '/'
    url_suffix = environment.get_ci_status_url_suffix()
    return base_url + url_suffix

def create_post_json(data, step, step_value, severity, description):
    return {
        'reportingService': 'evolene',
        'serviceName': data[pipeline_data.IMAGE_NAME],
        'serviceVersion': data[pipeline_data.IMAGE_VERSION],
        'stepName': step,
        'stepStatus': step_value,
        'severity': severity,
        'description': description,
        'environment': 'all'
    }

def post_unit_tests_run(data, step_status, severity, description = None):
    post(data, 'UNIT_TESTS', step_status, severity, description)

def post_integration_tests_run(data, step_status, severity, description = None):
    post(data, 'INTEGRATION_TESTS', step_status, severity, description)

def post_platform_validation_run(data, step_status, severity, description = None):
    if is_docker_pipeline(data):
        post(data, 'PLATFORM_VALIDATION', step_status, severity, description)

def post_local_build(data, step_status, severity, description = None):
    if is_docker_pipeline(data):
        post(data, 'LOCAL_BUILD', step_status, severity, description)

def post_ci_environment_run(data, step_status, severity, description = None):
    post(data, 'CI_ENVIRONMENT', step_status, severity, description)

def post_repo_security_scan_run(data, step_status, severity, description = None):
    post(data, 'REPO_SECURITY_SCAN', step_status, severity, description)

def post_pushed_to(data, step_status, severity, description = None):
    if is_docker_pipeline(data):
        post(data, 'PUSHED_TO', step_status, severity, description)

def post_build_done(data, step_status, severity, description = None):
    if is_docker_pipeline(data):
        post(data, 'BUILD_DONE', step_status, severity, description)

def post_open_source(data, step_status, severity, description = None):
    if is_docker_pipeline(data):
        post(data, 'OPEN_SOURCE', step_status, severity, description)

def post_team(data, step_status, severity, description = None):
    if is_docker_pipeline(data):
        post(data, 'TEAM', step_status, severity, description)

def is_docker_pipeline(data):
    if data is None:
        return False
    if pipeline_data.IMAGE_NAME in data:
        return True
    return False
