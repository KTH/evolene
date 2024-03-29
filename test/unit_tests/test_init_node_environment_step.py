__author__ = 'tinglev'

from posix import environ
import unittest
import sys
from unittest import mock
from modules.pipeline_steps.init_node_environment_step import InitNodeEnvironmentStep
from modules.util.exceptions import PipelineException
from modules.util import environment, pipeline_data

class InitNodeEnvironmentStepTests(unittest.TestCase):

    def test_run_step(self):
        data = {pipeline_data.NPM_CONF_NODE_VERSION: 'lts/*'}
        step = InitNodeEnvironmentStep()
        if environment.is_local_unit_test():
            step.get_nvm_installed_version = mock.MagicMock()
            step.get_nvm_installed_version.side_effect = PipelineException('N/A\n')
            step.install_version = mock.MagicMock()
            step.disable_update_notifications = mock.MagicMock()
            step.run_step(data)
            step.install_version.assert_called_with('lts/*')
            
            step.install_version.reset_mock()
            step.get_nvm_installed_version.side_effect = PipelineException('Error!\n')
            sys.exit = mock.MagicMock()
            step.run_step(data)
            sys.exit.assert_called_once()
            step.install_version.reset_mock()       
            step.get_nvm_installed_version.side_effect = None
            step.get_nvm_installed_version.return_value = 'lts/*'
            step.run_step(data)
            step.install_version.assert_not_called()
        else:
            step.run_step(data)
