__author__ = 'tinglev'

import os
import unittest
from mock import patch, call
from modules.util.exceptions import PipelineException
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import slack

class ConcretePipelineStep(AbstractPipelineStep):

    def run_step(self, data):
        if not 'counter' in data:
            data['counter'] = 0
        data['counter'] += 1
        return data

    def get_required_env_variables(self):
        return ['TEST_ENV', 'TEST_ENV_2']

    def get_required_data_keys(self):
        return ['TEST_DATA', 'TEST_DATA_2']

class AbstractPipelineStepTests(unittest.TestCase):

    def test_get_step_name(self):
        cps = ConcretePipelineStep()
        self.assertEqual(cps.get_step_name(), 'ConcretePipelineStep')

    @patch.object(AbstractPipelineStep, 'handle_step_error')
    def test_step_data_is_ok(self, _):
        cps = ConcretePipelineStep()
        data = None
        self.assertFalse(cps.step_data_is_ok(data))
        data = {}
        self.assertFalse(cps.step_data_is_ok(data))
        data = {'TEST_DATA': 'value'}
        self.assertFalse(cps.step_data_is_ok(data))
        data = {'TEST_DATA': 'value', 'TEST_DATA_3': 'value'}
        self.assertFalse(cps.step_data_is_ok(data))
        data = {'TEST_DATA': 'value', 'TEST_DATA_3': 'value', 'TEST_DATA_2': 'value'}
        self.assertTrue(cps.step_data_is_ok(data))
        data = {'TEST_DATA': [], 'TEST_DATA_3': 'value', 'TEST_DATA_2': 'value'}
        self.assertTrue(cps.step_data_is_ok(data))

    @patch.object(AbstractPipelineStep, 'handle_step_error')
    def test_step_environment_ok(self, mock_handle):
        cps = ConcretePipelineStep()
        mock_warn = patch.object(cps.log, 'warning').start()
        self.assertFalse(cps.step_environment_ok())
        os.environ['TEST_ENV'] = ""
        os.environ['TEST_ENV_2'] = ""
        self.assertTrue(cps.step_environment_ok())
        self.assertEqual(mock_warn.call_count, 2)
        mock_warn.reset_mock()
        os.environ['TEST_ENV'] = "value"
        os.environ['TEST_ENV_2'] = "value"
        self.assertTrue(cps.step_environment_ok())
        mock_warn.assert_not_called()
        mock_handle.reset_mock()
        del os.environ['TEST_ENV']
        self.assertFalse(cps.step_environment_ok())
        mock_warn.assert_not_called()
        mock_handle.assert_called_once()

    @patch.object(AbstractPipelineStep, 'log_error')
    @patch.object(slack, 'send')
    def test_handle_step_error(self, _, mock_log_error):
        cps = ConcretePipelineStep()
        self.assertRaises(SystemExit, cps.handle_step_error, 'test', ex=Exception('ex'))
        cps.handle_step_error('test', fatal=False)
        calls = [
            call(cps.log.fatal, 'test', Exception('ex')),
            call(cps.log.error, 'test', None)
        ]
        mock_log_error.has_calls(calls)

    def test_set_next_step(self):
        cps1 = ConcretePipelineStep()
        cps2 = ConcretePipelineStep()
        cpsr = cps1.set_next_step(cps2)
        self.assertEqual(cps1.next_step, cps2)
        self.assertEqual(cpsr, cps2)

    @patch.object(AbstractPipelineStep, 'step_environment_ok')
    @patch.object(AbstractPipelineStep, 'step_data_is_ok')
    def test_run_pipeline_step(self, mock_data_ok, mock_env_ok):
        mock_data_ok.return_value = True
        mock_env_ok.return_value = True
        cps1 = ConcretePipelineStep()
        cps2 = ConcretePipelineStep()
        cps3 = ConcretePipelineStep()
        cps1.set_next_step(cps2)
        cps2.set_next_step(cps3)
        result = cps1.run_pipeline_step({})
        self.assertEqual(result['counter'], 3)
        self.assertRaises(PipelineException, cps1.run_pipeline_step, {'counter': 'error'})
