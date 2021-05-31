__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data

class NpmAuthorPolicy(AbstractPipelineStep):

    name = "Check  /package.json have 'author' and 'email' attributes"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.PACKAGE_JSON]

    def run_step(self, data):
        if not 'author' in data[pipeline_data.PACKAGE_JSON]:
            self.handle_step_error(
                '"author" must be set in package.json'
            )
        if (not 'name' in data[pipeline_data.PACKAGE_JSON]['author'] or
                not 'email' in data[pipeline_data.PACKAGE_JSON]['author']):
            self.handle_step_error(
                '"name" and "email" must be set for "author" in package.json'
            )
        self.log.debug('Author has name and email in package.json, continuing')
        self.step_ok()

        return data
