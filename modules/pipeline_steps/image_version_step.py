__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import image_version_util
from modules.util import pipeline_data

class ImageVersionStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [environment.BUILD_NUMBER, environment.GIT_COMMIT]

    def get_required_data_keys(self): # pragma: no cover
        return [pipeline_data.IMAGE_VERSION]

    def run_step(self, data): # pragma: no cover
        data[pipeline_data.SEM_VER] = self.get_sem_ver(data[pipeline_data.IMAGE_VERSION],
                                                       self.get_patch_version(data))
        data[pipeline_data.COMMIT_HASH] = environment.get_git_commit_clamped()

        data[pipeline_data.IMAGE_VERSION] = self.append_commit_hash(self.get_version(data[pipeline_data.SEM_VER]))
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
        if environment.is_main_branch():
            return "{}".format(sem_ver)

        return "{}-{}".format(slugify(environment.get_git_branch()), sem_ver)

    def append_commit_hash(self, tag):
        return '{}_{}'.format(tag, environment.get_git_commit_clamped())
        
def slugify(name):
    """Take some name (any string) and return a version-slug-safe variant of it."""
    # This could be done better with an external dependency,
    # but branch-names are probably ascii anyway.
    # "feature/slånbärsöl" will become "feature.sl.nb.rs.l", so it errs on the safe side.
    # If the result is an empty string, substitute "unknown"
    return re.sub('[^a-z0-9]+', '.', name.lower()).strip('.') or 'unknown'
