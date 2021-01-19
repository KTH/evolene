__author__ = 'tinglev'

import logging
import requests
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util import environment, pipeline_data
from modules.util import text_cleaner

def send(text, snippet=None, icon=':jenkins:', username='Build Server (Evolene)'):
    message = text
    if snippet:
        message = f'{message} ```{text_cleaner.clean(snippet)}```'
    for channel in environment.get_slack_channels():
        body = get_payload_body(channel, message, icon, username)
        call_slack_endpoint(body)

def send_to_slack(message, icon=':jenkins:', username='Build Server (Evolene)', clean=True):
    if clean:
        cleaned_message = text_cleaner.clean(message)
    for channel in environment.get_slack_channels():
        body = get_payload_body(channel, cleaned_message, icon, username)
        call_slack_endpoint(body)

def on_npm_publish(package_name, version, data):
    text = (f'*{package_name}* version *{version}* was successfully published to '
               f'https://www.npmjs.com/package/{package_name}')
    if pipeline_data.IGNORED_CRITICALS in data:
        criticals = data[pipeline_data.IGNORED_CRITICALS]
        text = f'{text} - WARNING! This build had {criticals} ignored criticals!'
    
    send(text, icon=":npm:")

def on_npm_no_publish(package_name, version):
    text = (f'*{package_name} {version}* already exists on :npm: '
               f'https://www.npmjs.com/package/{package_name}')
    send(text=text)

def on_successful_private_push_old(name, size):
    message = (f'*{name}* pushed to :key: private registry, size {size}.')
    send_to_slack(message, icon=':jenkins:')

def on_successful_private_push(name, size):
    message = (f'*{name}* pushed to :key: :azure: private registry, size {size}.')
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
        "text": f'{text} ',
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
