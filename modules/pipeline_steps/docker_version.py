__author__ = 'paddy'

import logging
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.exceptions import PipelineException
from modules.util import process
from modules.util import ci_status

class DockerVersion(AbstractPipelineStep):

    name = "Show Docker version"

    def __init__(self):
        AbstractPipelineStep.__init__(self)
        self.log = logging.getLogger(__name__)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            ci_status.post_ci_environment_run(data, ci_status.STATUS_CI_PLATTFORM_GITHUB)
            output = process.run_with_output('docker --version')
            self.log.info(output)
            self.step_ok()
            
        except PipelineException as install_ex:
            self.handle_step_error('Error while checking Docker version. ', install_ex)
        return data
