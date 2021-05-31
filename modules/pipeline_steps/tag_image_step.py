__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data
from modules.util import environment
from modules.util import image_version_util
from modules.util import artifact

class TagImageStep(AbstractPipelineStep):

    name = "Tag built Docker image with image versions."

    def get_required_env_variables(self): #pragma: no cover
        return [environment.REGISTRY_HOST]

    def get_required_data_keys(self): #pragma: no cover
        return [pipeline_data.LOCAL_IMAGE_ID, pipeline_data.IMAGE_VERSION, pipeline_data.IMAGE_NAME]

    def run_step(self, data): #pragma: no cover
        '''
        Tag images build with semver like "appname:1.2.3_abcdefg"

        If PUSH_PUBLIC=True then also tag image without git hash "appname:1.2.3"
        '''

        if pipeline_data.IMAGE_TAGS not in data:
            data[pipeline_data.IMAGE_TAGS] = []
        
        # Default tagging appname:1.2.3_abcdefg
        self.tag(image_version_util.get_image(data), data)
        
        if environment.get_push_public():
            # Default tagging appname:1.2.3
            self.tag(image_version_util.get_image_only_semver(data), data)
            # Default tagging appname:latest
            #self.tag(image_version_util.get_latest_tag(data), data)

        self.step_ok()
        
        return data

    def tag(self, tag, data): #pragma: no cover
        data[pipeline_data.IMAGE_TAGS].append(tag)
        self.log.info('Tagged image "%s" with "%s"', data[pipeline_data.LOCAL_IMAGE_ID], tag)
