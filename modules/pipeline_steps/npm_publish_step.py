__author__ = 'tinglev'

import json
import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, slack, nvm, environment
from modules.util import file_util

class NpmPublishStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.NPM_VERSION_CHANGED, pipeline_data.NPM_PACKAGE_VERSION, pipeline_data.NPM_PACKAGE_NAME]

    def write_updated_package_json(self, data):
        file_util.overwite('/package.json', json.dumps(data[pipeline_data.PACKAGE_JSON]))
        self.log.info('Wrote updated package.json to disc, ready for npm publish.')

    def add_build_information(self, data):
        data[pipeline_data.PACKAGE_JSON]["se.kth.gitBranch"] = environment.get_git_branch()
        data[pipeline_data.PACKAGE_JSON]["se.kth.gitCommit"] = environment.get_git_commit_clamped()
        data[pipeline_data.PACKAGE_JSON]["se.kth.buildDate"] = environment.get_time()

        return data

    def run_step(self, data):

        data = self.add_build_information(data)

        self.write_updated_package_json(data)

        if not environment.is_main_branch():
            self.log.info('Branch is not main branch, so no npm publish will be done.')
            slack.send_to_slack((f'The :git: branch *{data[pipeline_data.NPM_PACKAGE_NAME]} | '
                                     f' {environment.get_git_branch()}* '
                                     'is not a main branch, so no NPM publish will be done.'))
            return data
        
        if data[pipeline_data.NPM_VERSION_CHANGED]:
            self.log.info(
                'Package will be published. Local version is %s and '
                'latest version on npm before publish is %s', data[pipeline_data.NPM_PACKAGE_VERSION], data[pipeline_data.NPM_MAJOR_MINOR_LATEST])
            self.publish(data)
            slack.on_npm_publish(data[pipeline_data.NPM_PACKAGE_NAME], data[pipeline_data.NPM_PACKAGE_VERSION], data)
        else:
            self.log.info('Skipping npm publish, no version change.')
            #slack.on_npm_no_publish(data[pipeline_data.NPM_PACKAGE_NAME], data[pipeline_data.NPM_PACKAGE_VERSION])
                                    
        return data

    def publish(self, data):
        result = nvm.exec_npm_command(data, 'publish --access public', environment.get_project_root())
        self.log.debug('Result from npm publish was: "%s"', result)
