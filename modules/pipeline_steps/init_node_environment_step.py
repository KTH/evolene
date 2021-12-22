__author__ = 'tinglev'

import sys
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import nvm

class InitNodeEnvironmentStep(AbstractPipelineStep):

    name = "Install NodeJS version specified in npm.conf"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.NPM_CONF_NODE_VERSION]

    def run_step(self, data):
        conf_version = data[pipeline_data.NPM_CONF_NODE_VERSION]
        self.log.info('Requested node version is: "%s"', conf_version)
        try:
            output = self.get_nvm_installed_version(conf_version)
            
            if 'N/A' in output:
                self.install_version(conf_version)

        except PipelineException as nvm_ex:
            if 'N/A' in str(nvm_ex):
                self.log.info('Requested node version not installed; installing')
                self.install_version(conf_version)
            else:
                self.handle_step_error(
                    'Unhandled exception when getting installed '
                    'node version',
                    nvm_ex
                )
        except:
            self.log(f'Error: {sys.exc_info()[0]}')
        # Disable notifications about new versions to not mess up output
        self.disable_update_notifications(data)
        result = self.install_version("")
        self.log.info(f'Versions according to nvm {result}')

        result = nvm.exec_npm_command(data, 'version')
        self.log.info(f'Installed Node version is {result}')

        self.step_ok()
        return data

    def disable_update_notifications(self, data):
        nvm.exec_npm_command(data, "config set update-notifier false")

    def get_nvm_installed_version(self, version):
        return nvm.exec_nvm_command(f'version {version}')

    def install_version(self, version):
        try:
            self.log.info(f'Installing node {version}')
            result = nvm.exec_nvm_command(f'install --default {version}')
            self.log.info(f'{result}')
            
        except PipelineException as pipeline_ex:
            self.handle_step_error(
                'Exception when trying to install node version. '
                'Is NODE_VERSION in npm.conf set to a valid version?',
                pipeline_ex
            )
