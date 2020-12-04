__author__ = 'tinglev'

import unittest
from modules.pipeline_steps.unit_test_step import UnitTestStep

class UnitTestStepTests(unittest.TestCase):

    def test_filename(self):
        self.assertEqual(UnitTestStep.UNIT_TEST_COMPOSE_FILENAME, "/docker-compose-unit-tests.yml")