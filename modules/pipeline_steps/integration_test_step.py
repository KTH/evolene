__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import docker
from modules.util.exceptions import PipelineException
from modules.util import file_util
from modules.util import image_version_util
from modules.util import ci_status
from modules.util import pipeline_data

class IntegrationTestStep(AbstractPipelineStep):

    name = "Integration tests"

    INTEGRATION_TEST_COMPOSE_FILENAME = '/docker-compose-integration-tests.yml'

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        if not file_util.is_file(IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME):
            self.log.info('No file named "%s" found. No integration tests will be run.',
                          IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME)
            self.step_skipped()
            ci_status.post_integration_tests_run(data, ci_status.STATUS_MISSING, 5, f'No file {IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME} in repository.')
            return data

        self.run_integration_tests(data)
        self.step_ok()
        ci_status.post_integration_tests_run(data, "All tests passed", 0)

        return data


    def run_integration_tests(self, data):
        try:
            self.log.info(
                "Running integration tests in '%s'",
                IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME
            )
            output = docker.run_integration_tests(
                file_util.get_absolue_path(
                    IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME
                )
                , data
            )
            self.log.info(output)

        except Exception as ex:
            ci_status.post_integration_tests_run(data, ci_status.STATUS_ERROR, 10, str(ex))
            self.handle_step_error(
                    f'\n:rotating_light: <!here> {image_version_util.get_image(data)} *integration test(s) failed*, see <{environment.get_console_url()}|:github: Github Actions log here>.',
                    self.get_stack_trace_shortend(ex),
                )

    def get_stack_trace_shortend(self, exception):
        return str(exception).replace('`', ' ')[-1000:]