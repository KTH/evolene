__author__ = 'tinglev'

import re
import sys
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import docker
from modules.util.exceptions import PipelineException
from modules.util import slack

class BuildLocalStep(AbstractPipelineStep):

    name = "Build Docker image"
    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_VERSION, pipeline_data.IMAGE_NAME]

    def run_step(self, data):

        self.log.info(f'Started building 🐳 docker image {data[pipeline_data.IMAGE_NAME]}:{data[pipeline_data.IMAGE_VERSION]}. This might take some time depending on your what you are doing ...')
        try:
            image_id = self.run_build(data)
            image_grep_output = self.verify_built_image(image_id)
            size = self.get_image_size(image_grep_output)
            data[pipeline_data.IMAGE_SIZE] = size
            if size == '0' or size == 'N/A':
                raise PipelineException('Built image has no size')
            data[pipeline_data.LOCAL_IMAGE_ID] = image_id
            self.log.info('Built image with id "%s" and size "%s"', image_id, size)
        except: 
            self.handle_step_error("Unknown error when building Docker image.", sys.exc_info()[0])
        self.step_ok()
        return data

    def format_image_id(self, image_id):
        self.log.debug('Full image id is "%s"', image_id)
        image_id = image_id.replace('sha256:', '')
        return image_id[:12]

    def verify_built_image(self, image_id):
        image_grep_output = docker.grep_image_id(image_id)
        if not image_grep_output or image_id not in image_grep_output:
            self.handle_step_error('Could not find locally built image')
        self.log.debug('Grep for image id returned "%s"', image_grep_output.rstrip())
        return image_grep_output

    def get_image_size(self, image_grep_output):
        self.log.info('image_grep_output contains: "%s"', image_grep_output)
        # Size mesured in megabytes
        size = re.search(r'[0-9\.]+(MB|GB)', image_grep_output)
        if size:
            return size.group(0).strip()

        return 'N/A'

    def run_build(self, data):
        lbl_image_name = f'se.kth.imageName={data[pipeline_data.IMAGE_NAME]}'
        lbl_image_version = f'se.kth.imageVersion={data[pipeline_data.IMAGE_VERSION]}'

        build_args = data[pipeline_data.BUILD_ARGS]
        try:
            image_id = docker.build(build_args=build_args, labels=[lbl_image_name, lbl_image_version])
        except:
            slack.send(text=f'Failed to build Docker images for {lbl_image_name}:{lbl_image_version}', icon=":no_entry:", username='Docker build failed on Github Actions (Evolene)')
            self.handle_step_error(f'Failed to build Docker images for {lbl_image_name}:{lbl_image_version}', sys.exc_info()[0])
        return self.format_image_id(image_id)
