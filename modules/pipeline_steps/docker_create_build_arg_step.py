__author__ = 'bjofra'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data


class DockerCreateBuildArgStep(AbstractPipelineStep):

    name = "Add Docker build ARGS"

    def get_required_env_variables(self): # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        if environment.get_docker_build_args():
            data[pipeline_data.BUILD_ARGS] = environment.get_docker_build_args()
            self.log.info('Will use build ARGS in Docker build.')
            self.step_ok()
        else:
            data[pipeline_data.BUILD_ARGS] = None
            self.log.info('No build ARGS passed to Docker build.')
            self.step_skipped()
        return data
