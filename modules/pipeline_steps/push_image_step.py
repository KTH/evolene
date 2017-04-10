__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment

class PushImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.REGISTRY_HOST, Environment.IMAGE_NAME]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        # docker push $REGISTRY_IMAGE_NAME
        # REGISTRY_IMAGE_NAME = REPO_HOST/IMAGE_NAME
        # Verify pushed image exists in repo
        return data
