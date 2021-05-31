__author__ = 'tinglev'

import time
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, docker, environment, file_util, image_version_util
from modules.util.exceptions import PipelineException

class DryRunStep(AbstractPipelineStep):

    DRY_RUN_COMPOSE_FILENAME = '/docker-compose-dry-run.yml'

    def __init__(self):
        super(DryRunStep, self).__init__()
        self.timeout = 60
        self.sleep = 5

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.LOCAL_IMAGE_ID]

    def run_step(self, data):
        if environment.use_dry_run():
            if not file_util.is_file(DryRunStep.DRY_RUN_COMPOSE_FILENAME):
                self.simple_dry_run(data)                
            else:
                self.compose_dry_run(data)
            self.step_ok()
        else:
            self.step_skipped()
            
        return data

    def compose_dry_run(self, data):
        self.log.info('Doing a dry run using "/docker-compose.yml" to test the newly built Docker iamge')
        try:
            output = docker.run_dry_run_compose(
                file_util.get_absolue_path(
                    DryRunStep.DRY_RUN_COMPOSE_FILENAME
                ), data
            )
            self.log.debug('Output from dry run was: %s', output)
        except Exception as ex:
            raise PipelineException(str(ex), self.get_slack_message(ex, data))

    def get_slack_message(self, exception, data):
        return '*{}* Compose dry run failed: \n```...\n{}```\n:jenkins: {}/console'.format(
            image_version_util.get_image(data),
            str(exception).replace('`', ' ')[-1000:],
            environment.get_build_url())

    def simple_dry_run(self, data):
        self.log.info('Doing a "docker run" dry start of the newly built Docker iamge')
        container_id = self.start_container(data)
        try:
            container_status = self.wait_for_container_created(container_id)
            if not self.is_running(container_status):
                self.handle_step_error(
                    '<!channel> Failed to test run the newly built container on Jenkins. '
                    'To disable test set Evolene env `SKIP_DRY_RUN="True"`'
                )
        finally:
            self.stop_container(container_id)
            self.log.info(
                'Dry run of image with id "%s" successful',
                data[pipeline_data.LOCAL_IMAGE_ID]
            )

    def get_container_status(self, container_id): #pragma: no cover
        return docker.get_container_status(container_id)

    def start_container(self, data): #pragma: no cover
        return docker.run(data[pipeline_data.LOCAL_IMAGE_ID])

    def wait_for_container_created(self, container_id):
        container_status = self.get_container_status(container_id)
        wait_remaining = self.timeout
        while self.is_creating(container_status) and wait_remaining > 0:
            self.log.debug('Container is creating. Waiting for status change..')
            time.sleep(self.sleep)
            wait_remaining -= self.sleep
            container_status = self.get_container_status(container_id)
        return container_status

    def is_running(self, container_status):
        # created|restarting|running|removing|paused|exited|dead
        return container_status == 'running'

    def is_creating(self, container_status):
        # created|restarting|running|removing|paused|exited|dead
        return container_status == 'created'

    def stop_container(self, container_id): #pragma: no cover
        docker.stop_and_remove_container(container_id)
