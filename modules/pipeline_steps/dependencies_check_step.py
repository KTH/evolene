__author__ = 'tinglev@kth.se'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import docker
from modules.util import process
from modules.util import environment
from modules.util import pipeline_data
from modules.util import file_util
from modules.util.exceptions import PipelineException
from modules.util import slack
from modules.util import npm_dependencies

class DependenciesCheckStep(AbstractPipelineStep):

    def get_required_env_variables(self):  # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):  # pragma: no cover
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION]

    def run_step(self, data):
        return npm_dependencies.run(data)
