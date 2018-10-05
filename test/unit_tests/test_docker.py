__author__ = 'tinglev'

import os
import unittest
from modules.util.environment import Environment
from modules.util.docker import Docker
from modules.util.process import Process
from modules.util.exceptions import PipelineException


class DockerTests(unittest.TestCase):

    IMAGE_ID = None
    CONTAINER_ID = None

    @classmethod
    def tearDownClass(cls):
        Process.run_with_output('docker rm -f {}'.format(DockerTests.CONTAINER_ID))
        Process.run_with_output('docker rmi -f {}'.format(DockerTests.IMAGE_ID))

    def test_all(self):
        try:
            self._test_build()
            self._test_tag_image()
            self._test_inspect_image()
            self._test_run()
            self._test_get_container_status()
            self._test_grep_image_id()
            self._test_stop_and_rm_container()
        except Exception as ex:
            print 'Error was: {}'.format(ex.message)
            self.tearDownClass()

    def test_grep_image_id_missing(self):
        self.assertRaises(PipelineException, Docker.grep_image_id, 'none-existing-image-id')

    def _test_build(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        test_lbl_1 = 'test.label.1=one'
        test_lbl_2 = 'test.label.2=two'
        result = Docker.build([test_lbl_1, test_lbl_2])
        DockerTests.IMAGE_ID = result.replace('sha256:', '')[:12]
        self.assertIn('sha256:', result)

    def _test_tag_image(self):
        Docker.tag_image(DockerTests.IMAGE_ID, 'test_tag')

    def _test_inspect_image(self):
        result = Docker.inspect_image(DockerTests.IMAGE_ID)
        self.assertIn('"test.label.1": "one"', result)
        self.assertIn('"test.label.2": "two"', result)
        self.assertIn('"test_tag:latest"', result)

    def _test_run(self):
        container_id = Docker.run(DockerTests.IMAGE_ID)
        DockerTests.CONTAINER_ID = container_id
        self.assertEqual(len(container_id), 64)

    def _test_get_container_status(self):
        status = Docker.get_container_status(DockerTests.CONTAINER_ID)
        self.assertEqual(status, 'running')

    def _test_grep_image_id(self):
        grep_return = Docker.grep_image_id(DockerTests.IMAGE_ID)
        self.assertTrue(DockerTests.IMAGE_ID in grep_return)
        # Test that the tag from the earlier step also appears here
        self.assertTrue('test_tag' in grep_return)
        image_id = Docker.grep_image_id('SHOULDNOTEXIST')
        self.assertIsNone(image_id)


    def _test_stop_and_rm_container(self):
        Docker.stop_and_remove_container(DockerTests.CONTAINER_ID)
        self.assertRaises(PipelineException, Docker.get_container_status, DockerTests.CONTAINER_ID)
