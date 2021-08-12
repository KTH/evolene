__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import image_version_util
from modules.util import file_util


class BuildEnvironmentToFileStep(AbstractPipelineStep):

    name = "Write build information to file before building image"

    def get_required_env_variables(self):
        return [environment.GIT_BRANCH, environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_VERSION, pipeline_data.IMAGE_NAME]

    def run_step(self, data):
        if environment.get_build_information_output_file():
            self.write(data)
            self.step_ok()
        else:
            self.step_skipped()

    def get_ouput_file(self):
        return environment.get_build_information_output_file()

    def write(self, data):
        try:
            file_util.overwite(self.get_ouput_file(), self.get_output(data))
            self.log.info(f'Wrote build information to {self.get_ouput_file()}')

        except IOError:
            self.handle_step_error("*{}* Unable to write build information to file '{}'".format(
                image_version_util.get_image(data),
                self.get_ouput_file()))

    def get_output(self, data):
        output_file = self.get_ouput_file()

        if str(output_file).endswith(".js"):
            return self.to_js_module(data)
        if str(output_file).endswith(".json"):
            return self.to_json(data)
        if str(output_file).endswith(".ts"):
            return self.to_ts_const(data)
        if str(output_file).endswith(".conf"):
            return self.to_conf(data)
        if str(output_file).endswith(".html"):
            return self.to_html(data)

    def to_ts_const(self, data):
        return "export const buildInfo = {}".format(json.dumps(self.get_build_environment(data)))

    def to_json(self, data):
        return json.dumps(self.get_build_environment(data))

    def to_js_module(self, data):
        return "module.exports = {}".format(json.dumps(self.get_build_environment(data)))

    def to_html(self, data):
        result = "<!DOCTYPE html><html><head><title>About</title></head><body><dl>"
        envs = self.get_build_environment(data)
        for env in envs:
            result += "<dt>{}:</dt><dd>{}</dd>".format(env, envs[env])
        result += "</dl></body></html>"
        return result

    def to_conf(self, data):
        result = ""
        envs = self.get_build_environment(data)
        for env in envs:
            result += "{}={}\n".format(env, envs[env])
        return result

    def get_build_environment(self, data):

        return {
            "gitBranch": environment.get_git_branch(),
            "gitCommit": environment.get_git_commit(),
            "gitUrl": environment.get_git_url(),
            "jenkinsBuild": environment.get_build_number(),
            "jenkinsBuildDate": environment.get_time(),
            "dockerName": data[pipeline_data.IMAGE_NAME],
            "dockerVersion": data[pipeline_data.IMAGE_VERSION],
            "dockerImage": image_version_util.prepend_registry(image_version_util.get_image(data))
        }
