__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import (environment, docker, 
                          file_util, image_version_util,
                          ci_status, pipeline_data)

class UnitTestStep(AbstractPipelineStep):

    name = "Unit tests"
    UNIT_TEST_COMPOSE_FILENAME = '/docker-compose-unit-tests.yml'

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):

        if not file_util.is_file(UnitTestStep.UNIT_TEST_COMPOSE_FILENAME):
            self.log.info('No file named "%s" found. No unit tests will be run.',
                          UnitTestStep.UNIT_TEST_COMPOSE_FILENAME)
            self.step_skipped()
            ci_status.post_unit_tests_run(data, ci_status.STATUS_MISSING, 5)
            return data

        self.run_unit_tests(data)
        self.step_ok()
        ci_status.post_unit_tests_run(data, ci_status.STATUS_OK, 0)

        return data

    def run_unit_tests(self, data):
        self.log.info("Running unit tests")

        try:
            output = docker.run_unit_test_compose(
                file_util.get_absolue_path(
                    UnitTestStep.UNIT_TEST_COMPOSE_FILENAME
                ), data
            )
            self.log.info(output)
        except Exception as ex:
            ci_status.post_unit_tests_run(data, ci_status.STATUS_ERROR, 10)
            self.handle_step_error(
                f'\n:rotating_light: <!here> {image_version_util.get_image(data)} *unit test(s) failed*, see <{environment.get_console_url()}|:github: Github Actions log here>.',
                ex)
