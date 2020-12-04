__author__ = 'tinglev'

import logging
import requests
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util import environment, pipeline_data

def send_to_slack(message, icon=':jenkins:', username='Build Server (Evolene)'):
    for channel in environment.get_slack_channels():
        body = get_payload_body(channel, message, icon, username)
        call_slack_endpoint(body)

def on_npm_publish(application, version, data):
    message = (f'*{application}* version *{version}* was successfully published to '
               f'https://www.npmjs.com/package/{application}')
    if pipeline_data.IGNORED_CRITICALS in data:
        criticals = data[pipeline_data.IGNORED_CRITICALS]
        message = f'{message} - WARNING! This build had {criticals} ignored criticals!'
    send_to_slack(message, icon=':npm:')

def on_npm_no_publish(application, version):
    message = (f'*{application} {version}* already exists on :npm: '
               f'https://www.npmjs.com/package/{application}')
    send_to_slack(message, icon=':jenkins:')

def on_successful_private_push(name, size):
    message = (f'*{name}* pushed to :kth: private registry, size {size}.')
    send_to_slack(message, icon=':jenkins:')

def on_successful_public_push(name, image_name, image_size):
    message = (
        f'*{name}* pushed to :docker: public registry '
        f'https://hub.docker.com/r/kthse/{image_name}/tags/, '
        f'size {image_size}.'
    )
    send_to_slack(message, icon=':jenkins:')

def on_warning(message):
    send_to_slack(message, icon=':warning:')

def get_payload_body(channel, text, icon, username='Build Server (Evolene)'):
    body = {
        "channel": channel,
        "text": text,
        "username": username,
        "icon_emoji": icon
    }
    return body

def call_slack_endpoint(payload):
    log = logging.getLogger(__name__)
    try:
        web_hook = environment.get_slack_web_hook()
        return requests.post(web_hook, json=payload)
    except HTTPError as http_ex:
        log.error('Slack endpoint threw HTTPError with response "%s"', http_ex.response)
    except ConnectTimeout as timeout:
        log.error('Timeout while trying to post to Slack endpoint: "%s"', timeout)
    except RequestException as req_ex:
        log.error('Exception when trying to post to Slack endpoint: "%s"', req_ex)
