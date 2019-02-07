__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.process import Process

class NpmVersionChangedStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [Data.NPM_VERSION, Data.NPM_PACKAGE_NAME]

    def run_step(self, data):
        current_version = data[Data.NPM_VERSION]
        package_name = data[Data.NPM_PACKAGE_NAME]
        result = self.get_latest_version(package_name)
        data[Data.NPM_VERSION_CHANGED] = (current_version != result)
        self.log.debug('npm version has changed "%s"', data[Data.NPM_VERSION_CHANGED])
        return data

    def get_latest_version(self, package_name):
        return Process.run_with_output(f'npm show {package_name} version')
