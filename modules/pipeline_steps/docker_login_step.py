__author__ = 'tinglev'

from modules.util import docker
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment

class DockerLoginStep(AbstractPipelineStep):

    name = 'Logging into Docker registries'

    def get_required_env_variables(self): # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):

        if environment.is_run_inside_docker():
            self.log.info('Logging in to Docker Hub.')
            docker.login_public()

        if environment.get_push_github():
            self.log.info('Logging in to Github Container Registry.')
            docker.login_github()

        self.log.info('Logging in to Azure Container Registry.')
        docker.login_azure()

        self.step_ok()

        return data
