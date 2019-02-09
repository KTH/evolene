__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import process
from modules.util.exceptions import PipelineException
from modules.util import nvm

class NpmLoginStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT, environment.NPM_USER,
                environment.NPM_PASSWORD, environment.NPM_EMAIL]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        # npm login doesn't support non-interactive login, so we'll do this
        # through a docker image
        cmd = (f'docker run '
               f'-e NPM_USER="{environment.get_npm_user()}" '
               f'-e NPM_PASS="{environment.get_npm_password()}" '
               f'-e NPM_EMAIL="{environment.get_npm_email()}" '
               f'bravissimolabs/generate-npm-authtoken '
               f'> ~/.npmrc')
        try:
            result = process.run_with_output(cmd)
        except PipelineException as docker_ex:
            self.handle_step_error(
                'Exception when trying to get auth token from npm via docker',
                docker_ex
            )
        self.log.debug('Output from npm login was: "%s"', result)
        try:
            result = nvm.exec_npm_command(data, 'whoami')
        except PipelineException as npm_ex:
            self.handle_step_error(
                'Exception when trying to verify identify with npm whoami',
                npm_ex
            )
        self.log.debug('Output from npm whoami was: "%s"', result)
        return data
