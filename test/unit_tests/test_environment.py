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
