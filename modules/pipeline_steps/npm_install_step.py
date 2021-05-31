__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm

class NpmInstallStep(AbstractPipelineStep):

    name = "Install dependencies in /package.json"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            nvm.exec_npm_command(data, 'install')
        except PipelineException as npm_ex:
            self.handle_step_error(
                'Exception when trying to run npm install',
                npm_ex
            )
        self.log.info('Npm install completed successfully')
        self.step_ok()
        return data
