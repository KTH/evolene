__author__ = 'tinglev@kth.se'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.docker import Docker
from modules.util.process import Process
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.exceptions import PipelineException
from modules.util.slack import Slack

class RepoSupervisorStep(AbstractPipelineStep):

    IMAGE_NAME = 'repo-supervisor'
    EXCLUDED_DIRECTORIES = ['node_modules']

    def get_required_env_variables(self): #pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): #pragma: no cover
        return [Data.IMAGE_NAME, Data.IMAGE_VERSION]

    def run_step(self, data):
        image_name = RepoSupervisorStep.IMAGE_NAME
        self._pull_image_if_missing(image_name)
        output = self._run_supervisor(image_name)
        if output:
            self._process_supervisor_result(output, data)
        else:
            self.log.info('Repo-supervisor found nothing')
        return data

    def _pull_image_if_missing(self, image_name):
        image_grep_output = Docker.grep_image_id(image_name)
        if not image_grep_output or image_name not in image_grep_output:
            self.log.debug('Couldnt find local image "%s". Pulling from docker.io.',
                           image_name)
            Docker.pull(image_name)

    def _process_supervisor_result(self, cmd_output, data):
        results = json.loads(cmd_output)
        filenames = [f_name.replace('/opt/scan_me', '').encode('utf-8')
                     for (f_name, _)
                     in results['result'].iteritems()
                     if not self._directory_is_excluded(f_name)]
        if filenames:
            self._log_warning_and_send_to_slack(filenames, data)

    def _log_warning_and_send_to_slack(self, filenames, data):
        self.log.info('Found suspicious string in files "%s"', filenames)
        msg = ('Found suspicious string(s) in the following file(s) "{}" '
               'while building image "{}:{}"'
               .format(filenames, data[Data.IMAGE_NAME], data[Data.IMAGE_VERSION]))
        Slack.on_warning(msg)

    def _directory_is_excluded(self, filename):
        for directory in RepoSupervisorStep.EXCLUDED_DIRECTORIES:
            if directory in filename:
                return True
        return False

    def _run_supervisor(self, image_name):
        cmd = ('docker run --rm -v ${{WORKSPACE}}:/opt/scan_me {} '
               '/bin/bash -c "source ~/.bashrc && '
               'JSON_OUTPUT=1 node /opt/repo-supervisor/dist/cli.js /opt/scan_me"'
               .format(image_name))
        try:
            return Process.run_with_output(cmd)
        except PipelineException as pipeline_ex:
            # Special handling while waiting for https://github.com/auth0/repo-supervisor/pull/5
            if 'Not detected any secrets in files' not in pipeline_ex.message:
                self.log.warn('Ignoring error in repo supervisor step: "%s"', pipeline_ex.message)
            return None
