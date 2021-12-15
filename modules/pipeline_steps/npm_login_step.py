__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import process
from modules.util.exceptions import PipelineException
from modules.util import nvm
from modules.util import environment
from modules.util import file_util
class NpmLoginStep(AbstractPipelineStep):

    name = "Login to NPM registry with token"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT, environment.NPM_PUBLISH_TOKEN]

    def get_required_data_keys(self):
        return []

    def get_output_file(self):
        return f'{environment.get_home()}/.npmrc'

    def write_token_to_disc(self):
        file_util.append_absolute(self.get_output_file(), f"//registry.npmjs.org/:_authToken={environment.get_npm_publish_token()}")

    def run_step(self, data):
        self.log.debug('Logging in to NPM using token.')
        self.write_token_to_disc()
        self.step_ok()
        return data
