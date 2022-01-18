__author__ = 'tinglev'

import unittest
from unittest.mock import MagicMock
import os
from modules.pipeline_steps.open_source import OpenSourceStep
from modules.util import environment

class OpenSourceStepTest(unittest.TestCase):

    def test_closed(self):
        step = OpenSourceStep()
        os.environ[environment.GITHUB_REPOSITORY] = "KTH/search-api"
        self.assertFalse(step.is_public())

    def test_closed_when_404(self):
        step = OpenSourceStep()
        os.environ[environment.GITHUB_REPOSITORY] = "KTH/none-existing-repo"
        self.assertFalse(step.is_public())

    def test_open(self):
        step = OpenSourceStep()
        os.environ[environment.GITHUB_REPOSITORY] = "KTH/evolene"
        self.assertTrue(step.is_public())
