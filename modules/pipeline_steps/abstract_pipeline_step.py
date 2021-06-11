__author__ = 'tinglev'

import os
import sys
import logging
from abc import ABCMeta, abstractmethod
from modules.util.exceptions import PipelineException
from modules.util import slack
from modules.util import environment

class AbstractPipelineStep:
    __metaclass__ = ABCMeta
    next_step = None
    name = None

    def __init__(self):
        self.log = logging.getLogger("-")

    @abstractmethod
    def run_step(self, data): #pragma: no cover
        """ Should return data """

    @abstractmethod
    def get_required_env_variables(self): #pragma: no cover
        """ Should return a string array with the names of the environment
            variables required by the current step """
        return []

    @abstractmethod
    def get_required_data_keys(self): #pragma: no cover
        """ Should return a string array with the names of the keys
            that has to exist and have values in the data-object that
            is passed between build steps """
        return []

    def get_step_name(self):
        if self.name:
            return self.name

        return self.__class__.__name__

    def step_data_is_ok(self, data):
        for key in self.get_required_data_keys():
            if not data or not key in data:
                err = '"{}" missing data key "{}"'.format(self.get_step_name(), key)
                self.handle_step_error(err)
                return False
        return True

    def step_environment_ok(self):
        for env in self.get_required_env_variables():
            if not env in os.environ:
                err = '"{}" missing env variable "{}"'.format(self.get_step_name(), env)
                self.handle_step_error(err)
                return False
            if not os.environ.get(env):
                self.log.warning('Environment variable "%s" exists but is empty', env)
        return True

    def handle_step_error(self, message, ex=None, fatal=True):
        self.step_failed()
        error_func = self.log.error
        if fatal:
            error_func = self.log.fatal
        self.log_error(error_func, message, ex)
        self.report_error_to_slack(message, ex)
        if fatal:
            sys.exit(1)

    def log_error(self, error_func, message, ex): #pragma: no cover
        if ex:
            error_func(message, exc_info=True)
        else:
            error_func(message)

    def report_error_to_slack(self, message, ex):
        workspace = environment.get_project_root()
        if workspace:
            text = f'*{workspace}* \n{message}'

        slack.send(text=text, snippet=ex, icon=":no_entry:", username='Faild to build repository on Build Server (Evolene)')

    def run_pipeline_step(self, data):
        if not self.step_environment_ok():
            return data
        if not self.step_data_is_ok(data):
            return data
        try:
            self.run_step(data)
            
        except PipelineException as p_ex:
            p_ex.set_data(data)
        except Exception as ex:
            p_ex = PipelineException(str(ex), str(ex))
            p_ex.set_data(data)
            raise p_ex
        if self.next_step:
            self.next_step.run_pipeline_step(data)
        return data

    def set_next_step(self, next_step):
        self.next_step = next_step
        return next_step

    def _step_inform(self, passed="faild"):
        if "failed" in passed:
            self.log.fatal('🔴 %s. Step failed\n', self.get_step_name())
        elif "ok" in passed:
            self.log.info('🟢 %s. Done\n', self.get_step_name())
        elif "warning" in passed:
            self.log.warn('🟡 %s. Warning\n', self.get_step_name())
        else:
            self.log.info('⚪️ %s. Skipped\n', self.get_step_name())
        
    def step_ok(self):
        self._step_inform("ok")

    def step_skipped(self):
        self._step_inform("skipped")

    def step_failed(self):
        self._step_inform("failed")

    def step_warning(self):
        self._step_inform("warning")
