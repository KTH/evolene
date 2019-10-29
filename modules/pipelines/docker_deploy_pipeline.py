__author__ = 'tinglev'

import logging
import sys
from modules.pipeline_steps.docker_version import DockerVersion
from modules.pipeline_steps.setup_step import SetupStep
from modules.pipeline_steps.read_conf_step import ReadConfFileStep
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.pipeline_steps.build_local_step import BuildLocalStep
from modules.pipeline_steps.build_environment_to_file_step import BuildEnvironmentToFileStep
from modules.pipeline_steps.dry_run_step import DryRunStep
from modules.pipeline_steps.test_image_step import TestImageStep
from modules.pipeline_steps.tag_image_step import TagImageStep
from modules.pipeline_steps.push_image_step import PushImageStep
from modules.pipeline_steps.push_public_image_step import PushPublicImageStep
from modules.pipeline_steps.repo_supervisor_step import RepoSupervisorStep
from modules.pipeline_steps.unit_test_step import UnitTestStep
from modules.pipeline_steps.integration_test_step import IntegrationTestStep
from modules.pipeline_steps.from_image_step import FromImageStep
from modules.pipeline_steps.celebrate_step import CelebrateStep
from modules.pipeline_steps.docker_create_build_arg_step import DockerCreateBuildArgStep
from modules.pipeline_steps.done_step import DoneStep
from modules.util.exceptions import PipelineException
from modules.util import environment, print_util, slack, pipeline, pipeline_data

class DockerDeployPipeline(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)

        self.pipeline_steps = pipeline.create_pipeline_from_array([
            # Print Docker version
            DockerVersion(),
            # Configure pipeline
            SetupStep(),
            # Check the content of docker.conf
            ReadConfFileStep('docker.conf', [environment.IMAGE_NAME, pipeline_data.IMAGE_VERSION]),
            # Create new image version major.minor.path_githash
            ImageVersionStep(),
            # Check Dockerfile exists
            DockerFileStep(),
            # Check Dockerfiles FROM statement
            FromImageStep(),
            # Check that ENTRYPOINT is not used
            # InstructionStep()
            # Write information about the current build to a json-file.
            BuildEnvironmentToFileStep(),
            # Scan the repo for passwords, tokens or other suspicious looking strings
            RepoSupervisorStep(),
            # Create docker --build-arg
            DockerCreateBuildArgStep(),
            # Build the image to local registry
            BuildLocalStep(),
            # It never to late to party
            CelebrateStep(),
            # Test run the image
            DryRunStep(),
            # Run unit tests
            UnitTestStep(),
            # Run integration tests
            IntegrationTestStep(),
            # Do something (leftover?)
            TestImageStep(),
            # Tag the built image with image version
            TagImageStep(),
            # Push the tagged image to a repository
            PushPublicImageStep(),
            PushImageStep(),
            DoneStep()
        ])

    def run_pipeline(self):
        self.verify_environment()
        self.run_steps()

    def run_steps(self):
        try:
            self.log.info('Running Docker build pipeline')
            data = self.pipeline_steps[0].run_pipeline_step({})
        except PipelineException as p_ex:
            workspace = f'`{environment.get_project_root()}`'
            self.log.fatal('%s'.encode('UTF-8'), p_ex, exc_info=False)
            slack.send_to_slack(f'<!channel> {workspace}: \n {p_ex.slack_message}', username='Faild to build or test (Evolene)')
            print_util.red("Such bad, very learning.")
            sys.exit(1)
        else:
            self.log.info('Pipeline done. Pipeline data: %s', data)

    def verify_environment(self):
        try:
            self.log.info('Running environment verification')
            step = self.pipeline_steps[0]
            while step:
                step.step_environment_ok()
                step = step.next_step
        except PipelineException as p_ex:
            self.log.fatal('Caught exception: %s', p_ex, exc_info=True)
