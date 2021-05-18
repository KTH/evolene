__author__ = 'tinglev@kth.se'

import os
from modules.util import pipeline_data
from modules.util import process
from modules.util import environment

NVM_DIR = f'{environment.get_home()}/.nvm/nvm.sh'

def get_nvm_source():
    if environment.is_run_inside_docker():
        return ""

    return f'. {NVM_DIR} && '

def get_nvm_exec_base(data):
    nvm_source = get_nvm_source()
    conf_version = data[pipeline_data.NPM_CONF_NODE_VERSION]
    return (
        f'{nvm_source}'
        f'nvm exec --silent {conf_version}'
    )

def get_npm_base(data):
    nvm_base = get_nvm_exec_base(data)
    project_path = environment.get_project_root()
    return (
        f'{nvm_base} npm --prefix {project_path}'
    )

def run_npm_script(data, script_name):
    npm_base = get_npm_base(data)
    return process.run_with_output(
        f'{npm_base} run-script {script_name}'
    ).replace('\n', '').strip()

def exec_npm_command(data, command, flags=''):
    result = ''
    npm_base = get_npm_base(data)
    npm_command = f'{npm_base} {command} {flags}'
    output = process.run_with_output(npm_command)
    if output:
        result = output.replace('\n', '').strip()
    return result

def exec_nvm_command(command):
    nvm_source = get_nvm_source()
    return process.run_with_output(
        f'{nvm_source}nvm {command}'
    ).strip()
