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

    def __init__(self):
        self.log = logging.getLogger(self.get_step_name())

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
            if ex:
                message = f'*{workspace}* \n{message} \n ```\n{str(ex)}\n```'
            else:
                message = f'*`{workspace}`* {message}'
        slack.send_to_slack(message, username='Faild to build or test (Evolene)')

    def run_pipeline_step(self, data):
        if not self.step_environment_ok():
            return data
        if not self.step_data_is_ok(data):
            return data
        self.log.info('Running "%s"', self.get_step_name())
        try:
            self.run_step(data)
        except PipelineException as p_ex:
            p_ex.set_data(data)
            raise
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
