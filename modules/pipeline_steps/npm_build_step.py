__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data

class NpmBuildStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.NPM_CONF_NODE_VERSION]

    def run_step(self, data):
        try:
            result = nvm.run_npm_script(data, 'build')
        except PipelineException as npm_ex:
            self.handle_step_error(
                    f'\n:rotating_light: <!here> *NPM build failed*, see <{environment.get_console_url()}|:jenkins: Jenkins console log here>.',
                    self.get_stack_trace_shortend(npm_ex),
                )

        self.log.debug('Output from npm build was: "%s"', result)
        return data


    def get_stack_trace_shortend(self, exception):
        return str(exception).replace('`', ' ')[-1000:]