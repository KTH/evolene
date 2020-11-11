__author__ = 'tinglev'

import os
import unittest
from mock import MagicMock
from modules.pipeline_steps.push_image_step import PushImageStep
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import environment, docker, slack

class PushImageStepTests(unittest.TestCase):

    def test_verify_image_in_tags(self):
        pis = PushImageStep()
        data = {pipeline_data.IMAGE_VERSION: '1.1.23_2135'}
        pis.verify_image_version_in_tags(['1.1.23_2135', '1.2.0_1234'], data)
        self.assertRaises(PipelineException,
                          pis.verify_image_version_in_tags, ['1.1.23_2136', '1.2.0_1234'], data)

    def test_push_image(self):
        pis = PushImageStep()
        docker.push = MagicMock()
        slack.on_successful_private_push = MagicMock()
        os.environ[environment.REGISTRY_HOST] = 'kthregistryv2.sys.kth.se'
        data = {
            pipeline_data.IMAGE_VERSION: '1.2.0_1234',
            pipeline_data.IMAGE_NAME: 'kth-azure-app',
            pipeline_data.IMAGE_TAGS: [
                'reg.sys.kth.se/kth-azure-app:1.2.0',
                'reg.sys.kth.se/kth-azure-app:1.2.0_123cas',
                'reg.sys.kth.se/kth-azure-app:latest',
            ],
            pipeline_data.IMAGE_SIZE: '100mb'
        }
        pis.push_image(data)
        docker.push.assert_any_call('reg.sys.kth.se/kth-azure-app:1.2.0')
        docker.push.assert_any_call('reg.sys.kth.se/kth-azure-app:1.2.0_123cas')
        docker.push.assert_any_call('reg.sys.kth.se/kth-azure-app:latest')

    def test_create_registry_url(self):
        pis = PushImageStep()
        os.environ[environment.REGISTRY_HOST] = 'kthregistryv2.sys.kth.se'
        os.environ[environment.IMAGE_NAME] = 'kth-azure-app'
        data = {pipeline_data.IMAGE_VERSION: '1.2.0_1234', pipeline_data.IMAGE_NAME: 'kth-azure-app'}
        result = pis.create_registry_url(data)
        self.assertEqual(result, 'https://kthregistryv2.sys.kth.se/v2/kth-azure-app/tags/list')

    def test_create_registry_url_azure(self):
        pis = PushImageStep()
        os.environ[environment.PUSH_AZURE] = "True"
        os.environ[environment.REGISTRY_HOST] = 'kthregistryv2.sys.kth.se'
        os.environ[environment.IMAGE_NAME] = 'kth-azure-app'
        os.environ[environment.AZURE_REGISTRY_HOST] = 'testregistry.azurecr.io'
        data = {pipeline_data.IMAGE_VERSION: '1.2.0_1234', pipeline_data.IMAGE_NAME: 'kth-azure-app'}
        result = pis.create_registry_url(data)
        self.assertEqual(result, 'https://testregistry.azurecr.io/acr/v1/kth-azure-app/_tags')
