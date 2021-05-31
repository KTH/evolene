__author__ = 'tinglev@kth.se'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import docker
from modules.util import process
from modules.util import environment
from modules.util import pipeline_data
from modules.util import file_util
from modules.util.exceptions import PipelineException
from modules.util import slack

class RepoSupervisorStep(AbstractPipelineStep):

    name = "Scan source code for password and tokens"

    SCANIGNORE_FILE = '/.scanignore'
    REPO_SUPERVISOR_IMAGE_NAME = 'kthse/repo-supervisor'
    REPO_MOUNTED_DIR = '/opt/scan_me'
    DEFAULT_PATTERNS = [
        '/node_modules/'
    ]

    def get_required_env_variables(self):  # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):  # pragma: no cover
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION]

    def run_step(self, data):
        image_name = RepoSupervisorStep.REPO_SUPERVISOR_IMAGE_NAME
        self._pull_image_if_missing(image_name)
        output = self._run_supervisor(image_name)
        if output:
            filenames = self._process_supervisor_result(output, data)
            if filenames:
                self.step_warning()

        else:
            self.log.info('Security scanning found nothing that looked like passwords or tokens in the source code.')
            self.step_ok()

        return data

    def _pull_image_if_missing(self, image_name):
        image_grep_output = None
        try:
            image_grep_output = docker.grep_image_id(image_name)

            if not image_grep_output or image_name not in image_grep_output:
                self.pull_image(image_name)

        except PipelineException:
            self.pull_image(image_name)

    def pull_image(self, image_name):
        self.log.debug(
            'Couldnt find local image "%s". Pulling from docker.io.', image_name)
        docker.pull(image_name)

    def _process_supervisor_result(self, cmd_output, data):
        results = json.loads(cmd_output)
        filenames = [result['filepath']
                     .replace(RepoSupervisorStep.REPO_MOUNTED_DIR, '')
                     .encode('utf-8')
                     for result
                     in results['result']
                     if not self.ignore(result['filepath'])]
        if filenames:
            self._log_warning_and_send_to_slack(filenames, data)
        return filenames

    def _log_warning_and_send_to_slack(self, filenames, data):
        self.log.warning('Found suspicious string in files "%s"', filenames)
        text = (f':rotating_light: <!here> *Possible password or token* in the following *{data[pipeline_data.IMAGE_NAME]}* file(s). \n'
               'If ok, remove the warning by adding the file, or catalog to `/.scanignore`.')
        slack.send(text=text, snippet=self.format_filnames(filenames), username="Code Security, Build Server (Evolene)")

    def format_filnames(self, filenames):
        result = ''
        for filename in filenames:
            result = "{}{}\n".format(result, filename.decode("utf-8"))
        return result

    def get_ignore_patterns(self):
        result = file_util.get_lines(RepoSupervisorStep.SCANIGNORE_FILE)
        result.extend(RepoSupervisorStep.DEFAULT_PATTERNS)

        return result

    def ignore(self, filename):
        # Inside the Repo scaner container the root is
        # /opt/scan_me/
        for pattern in self.get_ignore_patterns():
            if str(filename).startswith(RepoSupervisorStep.REPO_MOUNTED_DIR + pattern):
                self.log.info(("Security scan found '%s' but its ignored since it is matches "
                               ".scanignore pattern '%s'."),
                              filename.replace(RepoSupervisorStep.REPO_MOUNTED_DIR, ""), pattern)
                return True
        return False

    def _run_supervisor(self, image_name):

        self.log.info('Checking source repository for passwords and tokens.')

        root =  file_util.get_project_root()
        if environment.is_run_inside_docker():
            root = environment.get_docker_mount_root()

        mounted_dir = RepoSupervisorStep.REPO_MOUNTED_DIR

        cmd = (f'docker run --rm -v {root}:{mounted_dir} {image_name} /bin/bash -c "source ~/.bashrc && JSON_OUTPUT=1 node /opt/repo-supervisor/dist/cli.js {mounted_dir}"')
            
        try:
            # Do note that if your have packages installed like (/node_modules) this will probably break with
            # char encoding problems.
            return process.run_with_output(cmd)
        except PipelineException as pipeline_ex:
            # Special handling while waiting for https://github.com/auth0/repo-supervisor/pull/5
            if 'Not detected any secrets in files' not in str(pipeline_ex):
                self.log.warning(
                    'Ignoring error in repo supervisor step: "%s"', str(pipeline_ex)
                )
            return None
