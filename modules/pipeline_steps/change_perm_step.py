__author__ = 'tinglev'
import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, environment, process

class ChangePermStep(AbstractPipelineStep):

    name = "Change project dir permissions"

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        project_dir = environment.get_project_dir()
        (owner, _) = self.save_dir_owner(data, project_dir)
        if owner != 0:
            self.set_dir_owner(project_dir, 0, 0)
        self.step_ok()
        return data

    def save_dir_owner(self, data, project_dir):
        dir_info = os.stat(project_dir)
        data[pipeline_data.PROJECT_FILES_OWNER] = dir_info.st_uid
        data[pipeline_data.PROJECT_FILES_GROUP] = dir_info.st_gid
        return (dir_info.st_uid, dir_info.st_gid)

    def set_dir_owner(self, dir, owner, group):
        result = process.run_with_output(f'chown -hR {owner}:{group} {dir}')
        self.log.info(f'Change ownership of {dir} to {owner}:{group}: ', result)
