__author__ = 'paddy@kth.se'

import requests
from requests import HTTPError, ConnectTimeout, RequestException
import environment

def post(app_name, step, step_value):
    base_url = environment.get_ci_status_api_base_url()
    if base_url is None:
        return
    if not base_url.endswith('/'):
        base_url += '/'
    final_url = f'{base_url}evolene/{app_name}/{step}/{step_value}'
    try:
        return requests.post(final_url)
    except HTTPError as http_ex:
        log.error('ci-status endpoint threw HTTPError with response "%s"', http_ex.response)
    except ConnectTimeout as timeout:
        log.error('Timeout while trying to post to ci-status endpoint: "%s"', timeout)
    except RequestException as req_ex:
        log.error('Exception when trying to post to ci-status endpoint: "%s"', req_ex)
    