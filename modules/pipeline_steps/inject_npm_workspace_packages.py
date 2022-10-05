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

    name = "Build Docker image"
    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            # Read evolene-local-packages.json
            evolene_local_packages_json_path = file_util.get_absolue_path('/evolene-local-packages.json')
            has_evolene_local_packages_json = os.path.isfile(evolene_local_packages_json_path)

            if not has_evolene_local_packages_json:
                # This app doesn't have local packages to inject
                return data

            self.log.info(f'Found evolene-local-packages.json, injecting local workspace packages.')
            with open(evolene_local_packages_json_path) as f:
                local_packages = json.load(f)

            # Check if subdir evolene_local_packages/ exists
            evolene_local_packages_path = file_util.get_absolue_path('/evolene_local_packages')
            has_evolene_local_packages = os.path.isdir(evolene_local_packages_path)
            if not has_evolene_local_packages:
                os.mkdir(evolene_local_packages_path)

            # Copy local packages
            for package_name, pkg in local_packages.items():
                # Need to add leading slash to source path
                src = file_util.get_absolue_path(f"/{pkg.path}", from_repos_root=True)
                dest = file_util.get_absolue_path(f'/evolene_local_packages/{package_name}')
                shutil.copytree(src, dest, dirs_exist_ok=True)

        except:
            ci_status.post_local_build(data, ci_status.STATUS_ERROR, 10, text_cleaner.clean(sys.exc_info()[0]))
            self.handle_step_error("Error when injecting local NPM Workspace packages. Remove evolene-local-packages.json from your project to skip this step on next run.", sys.exc_info()[0])

        self.step_ok()
        return data
