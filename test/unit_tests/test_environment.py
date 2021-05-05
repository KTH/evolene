__author__ = 'tinglev'

import os
import unittest
from modules.util import environment
from modules.util import git

class EnvironmentTests(unittest.TestCase):

    def test_get_commit_clamped(self):
       
        os.environ[environment.GIT_COMMIT] = '1234567'
        result = git.get_commit_clamped()
        self.assertEqual(result, '1234567')
        
        os.environ[environment.GIT_COMMIT] = '1234567890'
        result = git.get_commit_clamped()
        self.assertEqual(result, '1234567')

        os.environ[environment.GIT_COMMIT] = '1234567890'
        result = git.get_commit_clamped(8)
        self.assertEqual(result, '12345678')
        
        os.environ[environment.GIT_COMMIT] = '1234'
        result = git.get_commit_clamped()
        self.assertEqual(result, '1234')

    def test_test_secrets(self):

        result = environment.get_tests_secrets()
        self.assertEqual(result, '')


        os.environ[environment.EVOLENE_TEST_SECRETS] = 'KEY_1=a KEY_2=b'
        result = environment.get_tests_secrets()
        self.assertEqual(result, 'KEY_1=a KEY_2=b')

        # Simultate a multiline input.
        multi_line ="""KEY_1=a
KEY_2=b"""

        os.environ[environment.EVOLENE_TEST_SECRETS] = multi_line
        result = environment.get_tests_secrets()
        self.assertEqual(result, 'KEY_1=a KEY_2=b')
