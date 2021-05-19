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

        self.log.info('Logging in to Docker Registries.')

        if environment.is_run_inside_docker():
            self.log.info('Logging in to Docker Hub.')
            docker.login_public()

        if (not environment.get_push_public()):
            self.log.info('Logging in to Private Docker Hub.')
            docker.login_private()

            if environment.get_push_azure():
                self.log.info('Logging in to Azure Container Registry.')
                docker.login_azure()

        return data
