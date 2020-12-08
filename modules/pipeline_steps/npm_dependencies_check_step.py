__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import npm_dependencies

class NpmDependenciesStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.PACKAGE_JSON]

    def run_step(self, data):
        npm_dependencies.run(data[pipeline_data.NPM_PACKAGE_NAME])
        return data