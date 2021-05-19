__author__ = 'tinglev'

from modules.util import docker
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import file_util

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
            self.log.info(file_util.read_as_string_absolute('/root/.docker/config.json'))
            

        if (not environment.get_push_public()):
            self.log.info('Logging in to Private Docker Hub.')
            docker.login_private()

            if environment.get_push_azure():
                self.log.info('Logging in to Azure Container Registry.')
                docker.login_azure()

        return data
