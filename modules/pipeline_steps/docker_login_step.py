__author__ = 'tinglev'

from modules.util import docker
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment

class DockerLoginStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        if environment.is_run_inside_docker():
            docker.login_public()
        if (not environment.get_push_public()):
            docker.login_private()
            if environment.get_push_azure():
                docker.login_azure()
        return data
