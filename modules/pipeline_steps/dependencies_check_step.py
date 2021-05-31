__author__ = 'tinglev@kth.se'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import npm_dependencies

class DependenciesCheckStep(AbstractPipelineStep):

    def get_required_env_variables(self):  # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):  # pragma: no cover
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION]

    def run_step(self, data):
        npm_dependencies.run(data[pipeline_data.IMAGE_NAME])
        self.step_ok()
        return data
