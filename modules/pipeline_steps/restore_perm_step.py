__author__ = 'tinglev'
import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, environment, process

class RestorePermStep(AbstractPipelineStep):

    name = "Restore project dir permissions"

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        project_dir = environment.get_project_dir()
        (owner, group) = self.get_old_dir_owner(data)
        self.set_dir_owner(project_dir, owner, group)
        self.step_ok()
        return data

    def get_old_dir_owner(self, data):
        return (data[pipeline_data.PROJECT_FILES_OWNER], data[pipeline_data.PROJECT_FILES_GROUP])

    def set_dir_owner(self, dir, owner, group):
        result = process.run_with_output(f'chown -hR {owner}:{group} {dir}')
        self.log.info(f'Change ownership of {dir} to {owner}:{group}: {result}')
