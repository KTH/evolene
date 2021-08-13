__author__ = 'tinglev'

import unittest
import os
from modules.util import environment
from modules.util import artifact

class ArtifactsTests(unittest.TestCase):

    def test_get_patch(self):
        os.environ[environment.GIT_BRANCH] = "origin/master"
        self.assertTrue(artifact.should_store())

    def test_get_2(self):
        os.environ[environment.GIT_BRANCH] = "freature/ns-34"
        os.environ[environment.BRANCHES_SAVE_STARTING_WITH] = "freature"
        self.assertTrue(artifact.should_store())
        del os.environ[environment.BRANCHES_SAVE_STARTING_WITH]

    def test_get_3(self):
        os.environ[environment.GIT_BRANCH] = "freature/ns-34"
        os.environ[environment.BRANCHES_SAVE_STARTING_WITH] = "pr-3"
        self.assertFalse(artifact.should_store())
        del os.environ[environment.BRANCHES_SAVE_STARTING_WITH]

    def test_get_4(self):
        os.environ[environment.GIT_BRANCH] = "freature/ns-34"
        self.assertTrue(artifact.branch_starts_with("freature"))

    def test_get_5(self):
        os.environ[environment.GIT_BRANCH] = "freature/ns-34"
        self.assertFalse(artifact.branch_starts_with(None))
