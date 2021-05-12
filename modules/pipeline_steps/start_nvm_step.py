__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import process
from modules.util import environment
from modules.util.exceptions import PipelineException

class StartNvmStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            #result = process.run_with_output('. /var/lib/jenkins/.nvm/nvm.sh && nvm --version')
            result = process.run_with_output(f'. {environment.get_home()}/.nvm/nvm.sh && nvm --version')
            
        except PipelineException as pipeline_ex:
            self.handle_step_error('Could not verify nvm version on jenkins', pipeline_ex)
        self.log.debug('nvm version is: "%s"', result.strip())
        return data
