__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, slack, nvm, environment
from modules.util import file_util
from modules.util import artifact
from modules.util import git


class NpmPublishStep(AbstractPipelineStep):

    name = "Publish the built NPM package"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.NPM_VERSION_CHANGED, pipeline_data.NPM_PACKAGE_VERSION, pipeline_data.NPM_PACKAGE_NAME]

    def write_updated_package_json(self, data):
        file_util.overwite(
            '/package.json', json.dumps(data[pipeline_data.PACKAGE_JSON]))
        self.log.info(
            'Wrote updated package.json to disc, ready for npm publish.')

    def add_build_information(self, data):
        data[pipeline_data.PACKAGE_JSON]["se.kth.gitBranch"] = environment.get_git_branch()
        data[pipeline_data.PACKAGE_JSON]["se.kth.gitCommit"] = git.get_commit_clamped()
        data[pipeline_data.PACKAGE_JSON]["se.kth.buildDate"] = environment.get_time()

        self.log.info('Added information to package.json')
        self.log.info(f'se.kth.gitBranch: {data[pipeline_data.PACKAGE_JSON]["se.kth.gitBranch"]}')
        self.log.info(f'se.kth.gitCommit: {data[pipeline_data.PACKAGE_JSON]["se.kth.gitCommit"]}')
        self.log.info(f'se.kth.buildDate: {data[pipeline_data.PACKAGE_JSON]["se.kth.buildDate"]}')

        return data

    def run_step(self, data):

        data = self.add_build_information(data)

        self.write_updated_package_json(data)

        if not artifact.should_store():
            self.log.info('Branch not to be publish to NPM.')
            slack.send((f'The :git: branch *{data[pipeline_data.NPM_PACKAGE_NAME]} | '
                                 f' {environment.get_git_branch()}* '
                                 'is not a main branch, nor configured to be push to the NPM registry.'))

            return data

        if data[pipeline_data.NPM_VERSION_CHANGED]:
            self.log.info(
                'Package will be published. Local version is %s and '
                'latest version on npm before publish is %s', data[pipeline_data.NPM_PACKAGE_VERSION], data[pipeline_data.NPM_MAJOR_MINOR_LATEST])
            #self.publish(data)
            slack.on_npm_publish(
                data[pipeline_data.NPM_PACKAGE_NAME], data[pipeline_data.NPM_PACKAGE_VERSION], data)
            #self.step_ok()
        else:
            self.log.info('Skipping npm publish, no version change.')
            slack.on_npm_no_publish(data[pipeline_data.NPM_PACKAGE_NAME], data[pipeline_data.NPM_PACKAGE_VERSION])
            self.step_skipped()

        return data

    def publish(self, data):
        result = nvm.exec_npm_command(
            data, 'publish --access public', environment.get_project_root())
        self.log.info('Result from npm publish was: "%s"', result)
