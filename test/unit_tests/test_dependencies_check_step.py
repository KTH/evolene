__author__ = 'tinglev'

import unittest
from modules.pipeline_steps.dependencies_check_step import DependenciesCheckStep

class DependenciesCheckStepTests(unittest.TestCase):

    def test_package_json_filename(self):
        self.assertEqual(DependenciesCheckStep.PACKAGE_JSON, "/package.json")

    def test_ncu_package_name(self):
        self.assertEqual(DependenciesCheckStep.IMAGE_NAME, "kthse/npm-package-available")

    def test_clean_removes_load_info(self):

        ncu_output = '''
           Checking /package.json
            [] 0/13 0%[] 1/13 7%[] 3/13 23%[] 6/13 46%[] 8/13 61%[] 9/13 69%[] 10/13 76%[] 11/13 84%[] 12/13 92%[] 13/13 100%
            mocha  ^8.2.0  →  ^8.2.1    
            
            Run  ncu -u  in the root of your project to update
            '''

        step = DependenciesCheckStep()

        self.assertFalse('[]' in step.clean(ncu_output))
        self.assertFalse('100%' in step.clean(ncu_output))


    def test_clean_removes_ncu_upgrade_info(self):

        ncu_output = '''
           Checking /package.json
            [] 0/13 0%[] 1/13 7%[] 3/13 23%[] 6/13 46%[] 8/13 61%[] 9/13 69%[] 10/13 76%[] 11/13 84%[] 12/13 92%[] 13/13 100%
            mocha  ^8.2.0  →  ^8.2.1    
            
            Run  ncu -u  in the root of your project to update
            '''

        step = DependenciesCheckStep()

        self.assertFalse('Run  ncu -u' in step.clean(ncu_output))