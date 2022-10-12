__author__ = 'tinglev'

import logging
import sys
from modules.pipeline_steps.setup_step import SetupStep
from modules.pipeline_steps.read_conf_step import ReadConfFileStep
from modules.pipeline_steps.change_perm_step import ChangePermStep
from modules.pipeline_steps.npm_build_step import NpmBuildStep
from modules.pipeline_steps.npm_test_step import NpmTestStep
from modules.pipeline_steps.npm_login_step import NpmLoginStep
from modules.pipeline_steps.load_package_json_step import LoadPackageJsonStep
from modules.pipeline_steps.npm_version_step import NpmVersionStep
from modules.pipeline_steps.npm_package_name_step import NpmPackageNameStep
from modules.pipeline_steps.npm_build_environment_to_file_step import NpmBuildEnvironmentToFileStep
from modules.pipeline_steps.npm_version_changed_step import NpmVersionChangedStep
from modules.pipeline_steps.npm_dependencies_check_step import NpmDependenciesStep
from modules.pipeline_steps.start_nvm_step import StartNvmStep
from modules.pipeline_steps.init_node_environment_step import InitNodeEnvironmentStep
from modules.pipeline_steps.npm_package_lock_step import NpmPackageLockStep
from modules.pipeline_steps.npm_audit_step import NpmAuditStep
from modules.pipeline_steps.npm_publish_step import NpmPublishStep
from modules.pipeline_steps.install_nvm_step import InstallNvmStep
from modules.pipeline_steps.npm_author_policy import NpmAuthorPolicy
from modules.pipeline_steps.npm_install_step import NpmInstallStep
from modules.pipeline_steps.restore_perm_step import RestorePermStep
from modules.pipeline_steps.done_step import DoneStep

from modules.util.exceptions import PipelineException
from modules.util import print_util, slack, pipeline_data, pipeline, environment


class NpmPipeline(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)
        # Configure pipeline
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            # Setup
            SetupStep(),
            # Set permissions on project dir so npm scripts runs as root
            ChangePermStep(),
            # Install nvm if not installed already
            # InstallNvmStep(), installed from docker file
            # Source nvm.sh and make sure nvm is executable
            # StartNvmStep(),
            # Read and parse the package.json file
            LoadPackageJsonStep(),
            # Make sure author exists and has name and email set
            NpmAuthorPolicy(),
            # Read and validate the npm.conf file
            ReadConfFileStep(
                'npm.conf', [pipeline_data.NPM_CONF_NODE_VERSION]),
            # Install the requested node version if missing in nvm
            InitNodeEnvironmentStep(),
            # Read the npm version from package.json
            NpmVersionStep(),
            # Read the npm package name from package.json
            NpmPackageNameStep(),
            # Check if the latest published version differs from this one
            NpmVersionChangedStep(),
            # Check old dependencies and inform
            # NpmDependenciesStep(),
            # Run npm install
            NpmInstallStep(),
            # Login to npm
            NpmLoginStep(),
            # Create our package.lock file
            NpmPackageLockStep(),
            # Run npm test
            NpmTestStep(),
            # Write information about the build to a file in the package.
            NpmBuildEnvironmentToFileStep(),
            # Run npm build
            NpmBuildStep(),
            # Run package audit
            NpmAuditStep(),
            # Publish the package if version has changed
            NpmPublishStep(),
            # Restore permissions of project directory so GitHub can cleanup
            RestorePermStep(),
            # Print done
            DoneStep()
        ])

    def run_pipeline(self):
        self.verify_environment()
        self.run_steps()

    def run_steps(self):
        try:
            self.log.info('Running npm pipeline')
            data = self.pipeline_steps[0].run_pipeline_step({})
        except PipelineException as p_ex:
            self.log.fatal('%s'.encode('UTF-8'), p_ex, exc_info=False)
            slack.send(f'<!here> *{environment.get_github_repository()}*',
                       snippet=p_ex.slack_message, username='Faild to build or test (Evolene)')
            print_util.red(f"{p_ex} - Such bad, very learning")
            sys.exit(1)

    def verify_environment(self):
        try:
            self.log.info('Running environment verification')
            step = self.pipeline_steps[0]
            while step:
                step.step_environment_ok()
                step = step.next_step
        except PipelineException as p_ex:
            self.log.fatal('Caught exception: %s', p_ex, exc_info=True)
