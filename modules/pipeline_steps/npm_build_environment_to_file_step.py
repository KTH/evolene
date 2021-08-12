__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import file_util
from modules.util import pipeline_data

class NpmBuildEnvironmentToFileStep(AbstractPipelineStep):

    name = "Write build information to file before building image"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.GIT_BRANCH, environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        self.write(data)
        self.step_ok()
        return data

    def get_ouput_file(self):
        return '/build-information.js'

    def write(self, data):
        try:
            self.log.info(f'Build information written {self.get_ouput_file()}, which will be included in published package.')
            file_util.overwite(self.get_ouput_file(), self.get_output(data))
        except IOError:
            self.handle_step_error("Unable to write npm build information to file '{}'".format(
                self.get_ouput_file()))

    def get_output(self, data):
        return self.to_js_module(data)

    def to_js_module(self, data):
        return "module.exports = {}".format(json.dumps(self.get_build_environment(data)))

    def get_build_environment(self, data):

        return {
            "gitBranch": environment.get_git_branch(),
            "gitCommit": environment.get_git_commit(),
            "gitUrl": environment.get_git_url(),
            "buildNumber": environment.get_build_number(),
            "buildDate": environment.get_time(),
            "version": data[pipeline_data.PACKAGE_JSON]["version"]
        }
