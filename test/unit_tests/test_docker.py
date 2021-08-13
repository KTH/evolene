__author__ = 'tinglev'

import os
import unittest
from modules.util import environment
from modules.util import docker
from modules.util import process
from modules.util.exceptions import PipelineException


class DockerTests(unittest.TestCase):

    IMAGE_ID = None
    CONTAINER_ID = None

    @classmethod
    def tearDownClass(cls):
        process.run_with_output('docker rm -f {}'.format(DockerTests.CONTAINER_ID))
        process.run_with_output('docker rmi -f {}'.format(DockerTests.IMAGE_ID))

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
            self.fail(str(ex))
            self.tearDownClass()

    def test_grep_image_id_missing(self):
        grep_return = docker.grep_image_id('none-existing-image-id')
        self.assertIsNone(grep_return)

    def _test_build(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        test_lbl_1 = 'test.label.1=one'
        test_lbl_2 = 'test.label.2=two'
        build_args = ['ARG1=test1', 'ARG2=test2']
        result = docker.build(build_args=build_args, labels=[test_lbl_1, test_lbl_2])
        DockerTests.IMAGE_ID = result.replace('sha256:', '')[:12]
        self.assertIn('sha256:', result)

    def _test_tag_image(self):
        docker.tag_image(DockerTests.IMAGE_ID, 'test_tag')

    def _test_inspect_image(self):
        result = docker.inspect_image(DockerTests.IMAGE_ID)
        self.assertIn('"test.label.1": "one"', result)
        self.assertIn('"test.label.2": "two"', result)
        self.assertIn('"test_tag:latest"', result)

    def _test_run(self):
        container_id = docker.run(DockerTests.IMAGE_ID)
        DockerTests.CONTAINER_ID = container_id
        self.assertEqual(len(container_id), 64)

    def _test_get_container_status(self):
        status = docker.get_container_status(DockerTests.CONTAINER_ID)
        self.assertEqual(status, 'running')

    def _test_grep_image_id(self):
        self.assertEqual(docker.grep_image_id(DockerTests.IMAGE_ID), DockerTests.IMAGE_ID)
        self.assertEqual(docker.grep_image_id('test_tag'), 'test_tag')
        self.assertIsNone(docker.grep_image_id('SHOULDNOTEXIST'))

    def _test_stop_and_rm_container(self):
        docker.stop_and_remove_container(DockerTests.CONTAINER_ID)
        self.assertRaises(PipelineException, docker.get_container_status, DockerTests.CONTAINER_ID)
