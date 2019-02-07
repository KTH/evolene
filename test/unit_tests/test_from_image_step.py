__author__ = 'tinglev'

import os
import unittest
from modules.util.environment import Environment
from modules.pipeline_steps.from_image_step import FromImageStep
from modules.util.data import Data

class DockerFileTests(unittest.TestCase):

    TEST_ALLOWED_IMAGES = {
        "kth-app": ["1.0", "2.0"],
        "kth-nodejs": ["9.11.0"],
        "other-app": ["latest"],
        "oracle": [],
        "redis": ["*"]
    }

    def test_docker_file_exists(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        fis = FromImageStep()
        result = fis.get_from_line()
        self.assertEqual("FROM redis", result)

    def test_supported_kth_image(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate(
            "FROM kthreg/kth-app:1.0", "kth-azure-app:13.37.0_abcdef"
        ))

    def test_not_supported_kth_image(self):
        self.assertFalse(FromImageStep(self.TEST_ALLOWED_IMAGES).validate(
            "FROM kthreg/kth-app:0.0", "kth-azure-app:13.37.0_abcdef"
        ))

    def test_more_supported_kth_image(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate(
            "FROM kthse/kth-nodejs:9.11.0", "kth-azure-app:13.37.0_abcdef"
        ))

    def test_other_app_image(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate(
            "FROM docker.io/other-app:latest", "kth-azure-app:13.37.0_abcdef"
        ))

    def test_allow_all_unknown_images(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate(
            "FROM docker.io/someimage:latest", "kth-azure-app:13.37.0_abcdef"
        ))

    def test_all_versions_invalid(self):
        self.assertFalse(FromImageStep(self.TEST_ALLOWED_IMAGES).validate(
            "FROM docker.io/oracle:11.1", "kth-azure-app:13.37.0_abcdef"
        ))

    def test_allow_all_versions(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate(
            "FROM docker.io/redis:13.37", "kth-azure-app:13.37.0_abcdef"
        ))

    def test_inform_if_change_image(self):
        data = {
            Data.IMAGE_NAME: "my-app",
            Data.IMAGE_VERSION: "1.2.3_abcdef"
        }
        self.assertIsNotNone(FromImageStep().get_change_image_message("kth-nodejs-api", data))
        self.assertIsNotNone(FromImageStep().get_change_image_message("kth-nodejs-web", data))

    def test_inform_if_change_image_is_empty(self):
        data = {
            Data.IMAGE_NAME: "my-app",
            Data.IMAGE_VERSION: "1.2.3_abcdef"
        }
        self.assertIsNone(FromImageStep().get_change_image_message(
            "should-not-return-a-message", data
            ))
