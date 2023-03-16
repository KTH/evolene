__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import docker
from modules.util import slack
from modules.util import artifact
from modules.util import ci_status
import os

class PushGithubImageStep(AbstractPipelineStep):

    name = 'Push to Github Packages'

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION, pipeline_data.SEM_VER, pipeline_data.IMAGE_TAGS, pipeline_data.LOCAL_IMAGE_ID]

    def run_step(self, data):
        if environment.get_push_github():
            if artifact.should_store():
                self.push_image(data)
                self.step_ok()
                ci_status.post_pushed_to(data, f'Public Github Packages', 0)
            else:
                self.log.info(
                    'Branch not to be published to Github Packages.')
                slack.send((f'The :git: branch *{data[pipeline_data.IMAGE_NAME]} | '
                                     f' {environment.get_git_branch()}* '
                                     'is not a main branch, nor configured to be push to Github Packages.'))
                ci_status.post_pushed_to(data, 'not pushed', 7, 'Branch not to be published to KTH registry')
                self.step_skipped()


        return data

    def push_image(self, data):
        for tag in data[pipeline_data.IMAGE_TAGS]:
            tag_with_registry = f"{environment.get_github_registry_host()}/{tag}"
            docker.tag_image(data[pipeline_data.LOCAL_IMAGE_ID], tag_with_registry)
            docker.push(tag_with_registry)
            slack.on_successful_public_push(tag, data[pipeline_data.IMAGE_NAME], data[pipeline_data.IMAGE_SIZE])
