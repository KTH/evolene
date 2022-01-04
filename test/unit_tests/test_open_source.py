__author__ = 'tinglev'

import unittest
from unittest.mock import MagicMock
import os
from modules.pipeline_steps.open_source import OpenSourceStep
from modules.util import environment

class OpenSourceStepTest(unittest.TestCase):

    def test_closed(self):
        step = OpenSourceStep()
        self.assertFalse(step.is_public('search-api'))

    def test_closed_when_404(self):
        step = OpenSourceStep()
        self.assertFalse(step.is_public('none-existing-repo'))

    def test_open(self):
        step = OpenSourceStep()
        self.assertTrue(step.is_public('evolene'))
