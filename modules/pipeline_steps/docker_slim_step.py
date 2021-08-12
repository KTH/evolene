__author__ = 'tinglev'

from os import environ, pipe
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import (
    pipeline_data,
    environment,
    process,
    image_version_util,
    docker
)

class DockerSlimStep(AbstractPipelineStep):

    name = "Beta: Minify Docker image "

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.LOCAL_IMAGE_ID]

    def run_step(self, data):
        if environment.get_slim():
            # Tag the image, otherwise we ger a bad reference error from docker build
            docker.tag_image(data[pipeline_data.LOCAL_IMAGE_ID], self.get_pre_slim_tag(data))
            self.run_docker_slim(data)
            # Get the image tage created by docker slim and set this as the new
            # image id and name
            data[pipeline_data.LOCAL_IMAGE_ID] = self.get_new_image_id(self.get_post_slim_tag(data))
            self.log.debug('Slimmed docker id is %s', data[pipeline_data.LOCAL_IMAGE_ID])
            data[pipeline_data.IMAGE_NAME] = f'{data[pipeline_data.IMAGE_NAME]}.slim'
        return data

    def get_pre_slim_tag(self, data):
        tag = image_version_util.prepend_registry(data[pipeline_data.IMAGE_NAME])
        tag = f'{tag}:pre_slim'
        return tag

    def get_post_slim_tag(self, data):
        tag = image_version_util.prepend_registry(data[pipeline_data.IMAGE_NAME])
        tag = f'{tag}.slim:latest'
        return tag

    def get_new_image_id(self, tag):
        return docker.get_image_id(tag)

    def run_docker_slim(self, data):
        env = environment.get_slim_env()
        if env:
            env = f'--env {env}'
        image_id = data[pipeline_data.LOCAL_IMAGE_ID]
        output = process.run_with_output(f'docker run --rm '
                                f'-v /var/run/docker.sock:/var/run/docker.sock '
                                f'dslim/docker-slim --in-container build {env} '
                                f'{image_id}')
        self.log.debug('Output from docker-slim was: %s', output)
