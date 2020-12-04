__author__ = 'tinglev@kth.se'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import docker
from modules.util import process
from modules.util import environment
from modules.util import pipeline_data
from modules.util import file_util
from modules.util.exceptions import PipelineException
from modules.util import slack

class DependeciesCheck(AbstractPipelineStep):

    PACKAGE_JSON = '/package.json'
    IMAGE_NAME = 'kthse/npm-package-available'

    def get_required_env_variables(self):  # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):  # pragma: no cover
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION]

    def run_step(self, data):

        if not file_util.is_file(DependeciesCheck.PACKAGE_JSON):
            self.log.info('No file named "%s" found. No dependencies check will be done.',
                          DependeciesCheck.PACKAGE_JSON)
            return data

        self.prepare()

        self.check(data)

        return data

    def prepare(self):
        self.pull_image_if_missing()

    def check(self, data):
        output = self.check_dependencies()
        if output:
            self.process_output(output, data)
        else:
            self.log.info('Got no output from dep checker.')

    def pull_image_if_missing(self):
        image_name = DependeciesCheck.IMAGE_NAME
        image_grep_output = None
        try:
            image_grep_output = docker.grep_image_id(image_name)

            if not image_grep_output or image_name not in image_grep_output:
                self.pull_image(image_name)

        except PipelineException:
            self.pull_image(image_name)

    def pull_image(self, image_name):
        self.log.debug(
            'Couldnt find local image "%s". Pulling from docker.io.', image_name)
        docker.pull(image_name)

    def process_output(self, cmd_output, data):

        # The ncu package checker itself needs an upgrade. Skip informing. Pls upgarde the docker image.
        if "Update available" in cmd_output:
            return

        # No deps in package.json
        if "No dependencies" in cmd_output:
            return

        # All is dandy
        if "All dependencies match the latest package" in cmd_output:
            return

        # Use only info after pattern "100%"
        upgrades_information = cmd_output[(cmd_output.index("100%") + len("100%")):]
        upgrades_information = cmd_output[:(cmd_output.index("Run"))]

        self.log_and_slack(upgrades_information, data)

    def log_and_slack(self, upgrades_information, data):
        self.log.info(
            'New dependencies version(s) available: \n %s', upgrades_information)
        if environment.use_experimental():
            msg = (f'*{data[pipeline_data.IMAGE_NAME]}* <https://www.npmjs.com/package/npm-check-updates|NPM Check Updates> reported new version(s) available. \n ```{upgrades_information}```\n Run `ncu -u` in the root of your project to update.')
            slack.send_to_slack(msg, icon=':jenkins:')

    def check_dependencies(self):
        image_name = DependeciesCheck.IMAGE_NAME
        cmd = f'docker run --tty --rm -v ${{WORKSPACE}}/package.json:/package.json {image_name}'
        try:
            return process.run_with_output(cmd)
        except PipelineException as pipeline_ex:
            self.log.warning(
                'Could not check dependencies: "%s"', str(pipeline_ex))
        return None
