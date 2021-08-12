__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data

class NpmTestStep(AbstractPipelineStep):

    name = "Unit tests"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.NPM_CONF_NODE_VERSION]

    def run_step(self, data):
        try:
            result = nvm.run_npm_script(data, 'test')
        except PipelineException as npm_ex:
            self.handle_step_error(
                'npm test failed',
                npm_ex
            )
        self.log.info('Output from npm test was: "%s"', result)
        self.step_ok()
        return data
