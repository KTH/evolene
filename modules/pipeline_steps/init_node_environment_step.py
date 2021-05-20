__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import nvm

class InitNodeEnvironmentStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.NPM_CONF_NODE_VERSION]

    def run_step(self, data):
        conf_version = data[pipeline_data.NPM_CONF_NODE_VERSION]
        self.log.debug('Requested node version is: "%s"', conf_version)
        try:
            self.get_nvm_installed_version(conf_version)
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
        self.log.debug('Node version %s installed with nvm', conf_version)
        return data

    def get_nvm_installed_version(self, version):
        return nvm.exec_nvm_command(f'version {version}')

    def install_version(self, version):
        try:
            nvm.exec_nvm_command(f'install {version}')
        except PipelineException as pipeline_ex:
            self.handle_step_error(
                'Exception when trying to install node version. '
                'Is NODE_VERSION in npm.conf set to a valid version?',
                pipeline_ex
            )
