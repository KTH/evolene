__author__ = 'tinglev'

import unittest
import os
from modules.util import artifact
from modules.util import environment

class ArtifactsTests(unittest.TestCase):

    def test_get_patch(self):
        os.environ[environment.GIT_BRANCH] = "origin/master"
        self.assertTrue(artifact.should_store())

    def test_get_2(self):
        os.environ[environment.GIT_BRANCH] = "freature/ns-34"
        os.environ[environment.ALSO_PUSH_BRANCHES_STARTING_WITH] = "freature"
        self.assertTrue(artifact.should_store())
        del os.environ[environment.ALSO_PUSH_BRANCHES_STARTING_WITH]

    def test_get_3(self):
        os.environ[environment.GIT_BRANCH] = "freature/ns-34"
        os.environ[environment.ALSO_PUSH_BRANCHES_STARTING_WITH] = "pr-3"
        self.assertFalse(artifact.should_store())
        del os.environ[environment.ALSO_PUSH_BRANCHES_STARTING_WITH]

