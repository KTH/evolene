__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import file_util

class ReadConfFileStep(AbstractPipelineStep):

    name = 'Read configuration file (docker.conf or npm.conf)'

    def __init__(self, conf_file_name, required_keys):
        AbstractPipelineStep.__init__(self)
        self.conf_file = f'/{conf_file_name}'
        self.required_keys = required_keys

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        data[pipeline_data.CONFIGURATION_FILE] = file_util.get_absolue_path(self.conf_file)
        self.log.info(f'Reading configurations in: {data[pipeline_data.CONFIGURATION_FILE]}')
        conf_lines = self.trim(file_util.get_lines(self.conf_file))
        if self.has_missing_conf_vars(conf_lines):
            self.handle_step_error('Missing the following configuration variables in `{}`: {}'
                                   .format(self.conf_file, self.get_missing_conf_vars(conf_lines)))
        data = self.add_conf_vars(conf_lines, data)
        self.step_ok()
        return data

    def clean_variable_value(self, value):
        return value.rstrip('"').lstrip('"')

    def add_conf_vars(self, env_lines, data):
        try:
            for env in env_lines:
                self.log.info('Adding %s value for: %s', self.conf_file, env.split('=')[0])
                data[env.split('=')[0]] = self.clean_variable_value(env.split('=')[1])
        except TypeError as t_err:
            self.log.warning('TypeError in add_conf_vars: %s', t_err, exc_info=True)
            return data
            
        self.inform(data)
        return data

    def inform(self, data):
        # docker.conf
        if pipeline_data.IMAGE_NAME in data and data[pipeline_data.IMAGE_NAME]:
            self.log.info(f'Docker image name: {data["IMAGE_NAME"]}')
        if pipeline_data.IMAGE_VERSION in data and data[pipeline_data.IMAGE_VERSION]:
            self.log.info(f'SemVer major.minor: {data["IMAGE_VERSION"]}')
            if pipeline_data.PATCH_VERSION not in data:
                self.log.info(f'Using timestamp as patchversion. You can specify a PATCH_VERSION in /docker.conf')
        if pipeline_data.PATCH_VERSION in data and data[pipeline_data.PATCH_VERSION]:
            self.log.info(f'SemVer patch: {data["PATCH_VERSION"]}')
            self.log.info(f'Using static patch version from docker.conf:s PATCH_VERSION instead of timestamp.')

        # npm.conf
        if pipeline_data.NPM_CONF_NODE_VERSION in data and data[pipeline_data.NPM_CONF_NODE_VERSION]:
            self.log.info(f'Running tests using Node {data["NODE_VERSION"]}.')
        if pipeline_data.NPM_CONF_ALLOW_CRITICALS in data and data[pipeline_data.NPM_CONF_ALLOW_CRITICALS]:
            self.log.info(f'Allow dependencies to contain critical vulnerabilities, change buy setting ALLOW_CRITICALS=False in /npm.conf')

    def trim(self, raw_lines):
        return [line for line in raw_lines
                if re.match(r'[^\s#="]+=(([^\s#="]+)|(".+"))$', line)]

    def has_missing_conf_vars(self, lines):
        if self.get_missing_conf_vars(lines):
            return True
        return False

    def get_missing_conf_vars(self, lines):
        try:
            variables = [line.split('=')[0] for line in lines]
            missing = [req for req in self.required_keys if req not in variables]
        except TypeError as t_err:
            self.log.warning('TypeError in missing conf vars: %s', t_err, exc_info=True)
            return self.required_keys
        return missing
