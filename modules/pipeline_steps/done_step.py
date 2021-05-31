__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import print_util


class DoneStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        self.log.info(data)
        print_util.green("\n🏁 🎉 Built, tested (you do have tests?) and pushed to registry!\n")
        return data
