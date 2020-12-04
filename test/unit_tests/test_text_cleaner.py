__author__ = 'tinglev'

import os
import unittest
from mock import MagicMock
from modules.pipeline_steps.unit_test_step import UnitTestStep
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import environment, docker, slack, text_cleaner

class UnitTestStepTests(unittest.TestCase):

    def test_regexp(self):
        ci_output = '''
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 |   1 passing (480ms)
        web_1_1b99cff96784 |   1 failing
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 |   1) Template handling
        web_1_1b99cff96784 |        Path '/_monitor' should contain 'No env value for ENV_TEST is set.' when env 'ENV_TEST' is not set.:
        web_1_1b99cff96784 |      AssertionError: expected '\n  - ENV_TEST: No env value for ENV_TEST is set. - Should return the cluster name.\n  - API Call: kth-azure-app - Should always return this applications name.\n  ' to include 'No env FAILJRED value for ENV_TEST is set'
        web_1_1b99cff96784 |       at Context.<anonymous> (/tests/unit-tests/test-app.js:22:23)
        web_1_1b99cff96784 |       at processTicksAndRejections (internal/process/task_queues.js:93:5)
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 | npm ERR! Test failed.  See above for more details.
        web_1_1b99cff96784 | kth-azure-app_web_1_1b99cff96784 exited with code 1
        Aborting on container exit...
        '''

        clean_text = text_cleaner.remove_docker_compose_output(ci_output)

        self.assertFalse('web_1_1b99cff96784 | ' in clean_text)
        self.assertTrue('1 failing' in clean_text)        

    def test_slack_message_shortend(self):
        ci_output = '''
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 |   1 passing (480ms)
        web_1_1b99cff96784 |   1 failing
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 |   1) Template handling
        web_1_1b99cff96784 |        Path '/_monitor' should contain 'No env value for ENV_TEST is set.' when env 'ENV_TEST' is not set.:
        web_1_1b99cff96784 |      AssertionError: expected '\n  - ENV_TEST: No env value for ENV_TEST is set. - Should return the cluster name.\n  - API Call: kth-azure-app - Should always return this applications name.\n  ' to include 'No env FAILJRED value for ENV_TEST is set'
        web_1_1b99cff96784 |       at Context.<anonymous> (/tests/unit-tests/test-app.js:22:23)
        web_1_1b99cff96784 |       at processTicksAndRejections (internal/process/task_queues.js:93:5)
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 | 
        web_1_1b99cff96784 | npm ERR! Test failed.  See above for more details.
        web_1_1b99cff96784 | kth-azure-app_web_1_1b99cff96784 exited with code 1
        Aborting on container exit...
        '''

        clean_text = text_cleaner.remove_possible_npm_standard_msg(ci_output)

        self.assertFalse('npm ERR!' in clean_text)
