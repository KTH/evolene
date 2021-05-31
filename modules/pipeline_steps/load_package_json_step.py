__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import file_util
from modules.util import pipeline_data

class LoadPackageJsonStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        package_content = file_util.read_as_string('/package.json')
        if package_content:
            data[pipeline_data.PACKAGE_JSON] = json.loads(package_content)
        else:
            self.handle_step_error('Could not load package.json for the project. '
                                   'Is the file missing or renamed?')
        self.step_ok()
        return data
