__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.exceptions import PipelineException
from modules.util import nvm

class NpmTestStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [Data.NPM_CONF_NODE_VERSION]

    def run_step(self, data):
        try:
            result = nvm.run_npm_script(data, 'test')
        except PipelineException as npm_ex:
            self.handle_step_error(
                'npm test failed',
                npm_ex
            )
        self.log.debug('Output from npm test was: "%s"', result)
        return data
