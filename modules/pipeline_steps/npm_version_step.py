__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data

class NpmVersionStep(AbstractPipelineStep):

    name = "Check /package.json have a 'version' attribute"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.PACKAGE_JSON]

    def run_step(self, data):
        try:
            npm_version = data[pipeline_data.PACKAGE_JSON]["version"]
        except KeyError as key_error:
            self.handle_step_error('Missing "version" in package.json', key_error)
        data[pipeline_data.NPM_PACKAGE_VERSION] = npm_version
        self.log.debug('npm version of application is "%s"', npm_version)
        self.step_ok()
        return data
