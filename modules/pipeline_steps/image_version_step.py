__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import git
from modules.util import image_version_util
from modules.util import pipeline_data
from modules.util import ci_status

class ImageVersionStep(AbstractPipelineStep):

    name = 'Calculate SemVer and final Docker image version'

    def get_required_env_variables(self): # pragma: no cover
        return [environment.BUILD_NUMBER, environment.GIT_COMMIT]

    def get_required_data_keys(self): # pragma: no cover
        return [pipeline_data.IMAGE_VERSION]

    def run_step(self, data): # pragma: no cover
        data[pipeline_data.SEM_VER] = self.get_sem_ver(data[pipeline_data.IMAGE_VERSION],
                                                       self.get_patch_version(data))
        data[pipeline_data.COMMIT_HASH] = git.get_commit_clamped()

        data[pipeline_data.IMAGE_VERSION] = self.append_commit_hash(self.get_version(data[pipeline_data.SEM_VER]))

        self.log.info(f'Bransh: {environment.get_git_branch()}')
        self.log.info(f'SemVer: {data[pipeline_data.SEM_VER]}')
        self.log.info(f'Git commit: {data[pipeline_data.COMMIT_HASH]}')
        self.log.info(f'Final image version: {data[pipeline_data.IMAGE_VERSION]}')

        # First place where we have image version need for CI-status
        ci_status.post_ci_environment_run(data, ci_status.STATUS_CI_PLATTFORM_GITHUB, 0)

        self.step_ok()
        
        return data

    def get_patch_version(self, data):
        if pipeline_data.PATCH_VERSION in data:
            return data[pipeline_data.PATCH_VERSION]
        return environment.get_build_number()

    def get_sem_ver(self, major_minor, patch_version):
        if not image_version_util.is_major_minor_only(major_minor):
            self.handle_step_error(('`/docker.conf` is invalid, replace *{}* with '
                                    'change to major.minor (no patch). Example: `IMAGE_VERSION="1.0"`')
                                   .format(major_minor))
        return "{}.{}".format(major_minor, patch_version)

    def get_version(self, sem_ver):
        if git.is_main_branch():
            return "{}".format(sem_ver)

        if environment.get_branches_tag_as_main():
            self.log.info(f'Branch is configured to be versioned as main {environment.BRANCHES_TAG_AS_MAIN}: True, so any branch name will not be added to the image tag.')
            return "{}".format(sem_ver)

        return "{}-{}".format(git.slugify_branch(), sem_ver)

    def append_commit_hash(self, tag):
        return '{}_{}'.format(tag, git.get_commit_clamped())

