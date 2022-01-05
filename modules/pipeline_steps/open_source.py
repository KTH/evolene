__author__ = 'tinglev'

import requests

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data, ci_status


class OpenSourceStep(AbstractPipelineStep):

    name = "Open or closed source on Github"

    def get_required_env_variables(self): # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        if self.is_public(data[pipeline_data.IMAGE_NAME]):
            self.log.info('%s is open source on Github.', data[pipeline_data.IMAGE_NAME])
            self.log.info('Repos name: %s\nImage name: %s', environment.get_github_repository(), environment.get_image_name())
            ci_status.post_open_source(data, 'Open Source', 0)
        else:
            self.log.info('Git repository is closed from public access.')
            ci_status.post_open_source(data, 'Closed', 5)

        self.step_ok()
         
        return data

    def is_public(self, image_name):
        if not image_name:
            return False
        try:
            response = requests.get(f'https://github.com/KTH/{image_name}')
            if response.status_code == 200:
                return True
        except:
            return False

        return False    