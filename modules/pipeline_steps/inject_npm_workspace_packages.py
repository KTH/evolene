__author__ = 'tinglev'

import sys
import os
import json
import shutil
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import file_util, text_cleaner
from modules.util import ci_status

# TODO: Consider more fine grained exception handling using PipelineException

class InjectNpmWorkspacePackages(AbstractPipelineStep):

    name = "Injecting Local Workspace Packages"
    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            # Check for evolene-sub-projects.json
            '''
            evolene-sub-projects.json:
            {
                "[sub-project-name]": {
                    "path": "[path/from/project/root]"
                }
            }
            NOTE: Project root is the folder containing the Dockerfile
            '''
            evolene_sub_projects_json_path = file_util.get_absolue_path('/evolene-sub-projects.json')
            has_evolene_sub_projects_json = os.path.isfile(evolene_sub_projects_json_path)

            if has_evolene_sub_projects_json:
                self.log.info(f'Found evolene-sub-projects.json, cheking each sub project.')
                with open(evolene_sub_projects_json_path) as f:
                    sub_projects = json.load(f)

                for sub_project_name, sub_prj in sub_projects:
                    self.log.info(f'Checking sub project "{sub_project_name}" at "{sub_prj["path"]}".')
                    tmpSubPath = sub_prj["path"].strip('/')
                    self.inject_local_packages(f'/{tmpSubPath}')
            else:
                self.log.info(f'Checking root of project.')
                self.inject_local_packages()

        except:
            ci_status.post_local_build(data, ci_status.STATUS_ERROR, 10, text_cleaner.clean(sys.exc_info()[0]))
            self.handle_step_error("Error when injecting local NPM Workspace packages. Remove evolene-local-packages.json from your project to skip this step on next run.", sys.exc_info()[0])

        self.step_ok()
        return data

    def inject_local_packages(self, sub_path = ""):
        # Read evolene-local-packages.json
        '''
            evolene-local-packages.json:
            {
                "[package-name]": {
                    "path": "[path/from/repos/root]"
                }
            }
        '''
        evolene_local_packages_json_path = file_util.get_absolue_path(f'{sub_path}/evolene-local-packages.json')
        has_evolene_local_packages_json = os.path.isfile(evolene_local_packages_json_path)

        if not has_evolene_local_packages_json:
            # This app doesn't have local packages to inject
            self.log.info(f'No evolene-local-packages.json file found.')
            self.step_skipped()
            return

        self.log.info(f'Found evolene-local-packages.json, injecting local workspace packages.')
        with open(evolene_local_packages_json_path) as f:
            local_packages = json.load(f)

        # Check if subdir evolene_local_packages/ exists
        evolene_local_packages_path = file_util.get_absolue_path(f'{sub_path}/evolene_local_packages')
        has_evolene_local_packages = os.path.isdir(evolene_local_packages_path)
        if not has_evolene_local_packages:
            os.mkdir(evolene_local_packages_path)

        # Copy local packages
        for package_name, pkg in local_packages.items():
            # Need to add leading slash to source path
            self.log.info(f'Injecting package "{package_name}" from "{pkg["path"]}"')
            src = file_util.get_absolue_path(f"/{pkg['path']}", from_repos_root=True)
            dest = file_util.get_absolue_path(f'{sub_path}/evolene_local_packages/{package_name}')
            shutil.copytree(src, dest, dirs_exist_ok=True)

