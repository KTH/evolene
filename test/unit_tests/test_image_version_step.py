__author__ = 'tinglev'

import unittest
from unittest import mock
import os
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.util import environment

class ImageVersionStepTests(unittest.TestCase):

    def test_format_image_version_with_build_number_as_patch(self):
        os.environ[environment.GIT_BRANCH] = 'origin/master'
        ivs = ImageVersionStep()
        result = ivs.get_sem_ver('1.2', 123)
        self.assertEqual(result, '1.2.123')

    def test_format_image_version_with_build_number_as_patch_and_hash(self):
        os.environ[environment.GIT_COMMIT] = "12345ai87q23b4sud6fyae"
        ivs = ImageVersionStep()
        self.assertEqual(ivs.append_commit_hash("1.2.123"), "1.2.123_12345ai")

    def test_format_image_version_to_long(self):
        os.environ[environment.GIT_BRANCH] = 'origin/master'
        ivs = ImageVersionStep()
        ImageVersionStep.handle_step_error = mock.MagicMock()
        ivs.get_sem_ver('1.2.321', 1)
        ImageVersionStep.handle_step_error.assert_called_once()

    def test_format_feature_branch_sem_ver(self):
        ivs = ImageVersionStep()
        os.environ[environment.GIT_BRANCH] = 'origin/a-feature-branch'
        feature_branch_version = ivs.get_sem_ver('2.3', 2)
        excepted = "2.3.2"
        self.assertEqual(feature_branch_version, excepted)

    def test_format_feature_branch(self):
        ivs = ImageVersionStep()
        os.environ[environment.GIT_BRANCH] = 'origin/a-feature-branch'
        feature_branch_version = ivs.get_version('2.3.2')
        excepted = "origin.a.feature.branch-2.3.2"
        self.assertEqual(feature_branch_version, excepted)

    def test_format_feature_branchand_hash(self):
        os.environ[environment.GIT_COMMIT] = "12345ai87q23b4sud6fyae"
        ivs = ImageVersionStep()
        self.assertEqual(ivs.append_commit_hash("origin.a.feature.branch-2.3.2"), "origin.a.feature.branch-2.3.2_12345ai")
