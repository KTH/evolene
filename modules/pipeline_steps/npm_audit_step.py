__author__ = 'tinglev'

import json
from json.decoder import JSONDecodeError
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data

class NpmAuditStep(AbstractPipelineStep):

    name = "NPM Audit on built /package-lock.json"

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            result = nvm.exec_npm_command(data, 'audit --json')
            audit_json = json.loads(result)
        except PipelineException as npm_ex:
            # npm audit returns a non-zero exit code on vulnerabilities
            try:
                # If the exception message is parsable as json
                # it's probably the output from the audit. We'll
                # check that it's ok later on
                audit_json = json.loads(str(npm_ex))
            except (ValueError, JSONDecodeError):
                # The error wasn't json - so this is probably a true
                # process error
                msg = 'npm audit failed'
                if 'Cannot audit a project without a lockfile' in str(npm_ex):
                    msg = ('Package.lock is missing, which is a required file '
                           'for npm audit to work. Maybe package-lock=false is '
                           'set in .npmrc?')
                self.handle_step_error(
                    msg,
                    npm_ex
                )
        data = self.approve_audit(data, audit_json)
        self.log.info('Audit result was "%s"', json.dumps(audit_json))
        self.step_ok()

        return data

    def approve_audit(self, data, audit_json):
        allow_criticals = False
        if pipeline_data.NPM_CONF_ALLOW_CRITICALS in data:
            allow_criticals = True
        criticals = self.get_criticals_from_audit(audit_json)
        if criticals > 0:
            self.log.debug('%s critical audit vulnerabilities found', criticals)
            if not allow_criticals:
                self.handle_step_error(
                    f'Package contains {criticals} critical vulnerabilities, aborting',
                )
            else:
                self.log.warning(
                    'Criticals exists, but ALLOW_CRITICALS is set; continuing'
                )
                data[pipeline_data.IGNORED_CRITICALS] = criticals
        self.log.debug('No critical vulernabilities found')
        return data

    def get_criticals_from_audit(self, audit_json):
        try:
            return audit_json['metadata']['vulnerabilities']['critical']
        except KeyError as key_err:
            self.handle_step_error('Error when parsing npm audit output', key_err)
 