__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import docker
from modules.util.exceptions import PipelineException

class BuildLocalStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_VERSION, pipeline_data.IMAGE_NAME]

    def run_step(self, data):
        image_id = self.run_build(data)
        image_grep_output = self.verify_built_image(image_id)
        size = self.get_image_size(image_grep_output)
        data[pipeline_data.IMAGE_SIZE] = size
        if size == '0' or size == 'N/A':
            raise PipelineException('Built image has no size')
        data[pipeline_data.LOCAL_IMAGE_ID] = image_id
        self.log.info('Built image with id "%s" and size "%s"', image_id, size)
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
        build_arg = data[pipeline_data.BUILD_ARG]
        image_id = docker.build(build_arg=build_arg, labels=[lbl_image_name, lbl_image_version])
        return self.format_image_id(image_id)
