__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data


class NpmPackageLockStep(AbstractPipelineStep):

    name = "Install package-lock.json only"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            if pipeline_data.NPM_CONF_LEGACY_PEER_DEPS in data:
                nvm.exec_npm_command(
                    data, 'install', '--package-lock-only --legacy-peer-deps')
            else:
                nvm.exec_npm_command(data, 'install --package-lock-only')
        except PipelineException as npm_ex:
            self.handle_step_error(
                'Exception when trying to install package.lock file',
                npm_ex
            )
        self.log.debug('Created package lock file')
        self.step_ok()
        return data
