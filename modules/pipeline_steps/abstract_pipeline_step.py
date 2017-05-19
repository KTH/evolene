__author__ = 'tinglev'

from abc import ABCMeta, abstractmethod
import os
import sys
import logging
from modules.util.slack import Slack
from modules.util.environment import Environment

class AbstractPipelineStep:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.log = logging.getLogger(self.get_step_name())
        self.next_step = None

    @abstractmethod
    def run_step(self, data): #pragma: no cover
        """ Should return data """
        pass

    @abstractmethod
    def get_required_env_variables(self): #pragma: no cover
        """ Should return a string array with the names of the environment
            variables required by the current step """
        pass

    @abstractmethod
    def get_required_data_keys(self): #pragma: no cover
        """ Should return a string array with the names of the keys
            that has to exist and have values in the data-object that
            is passed between build steps """
        pass

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
                self.log.warn('Environment variable "%s" exists but is empty', env)
        return True

    def handle_step_error(self, message, ex=None, fatal=True):
        error_func = self.log.error
        if fatal:
            error_func = self.log.fatal
        self.log_error(error_func, message, ex)
        self.report_error_to_slack(message)
        if fatal:
            sys.exit(1)

    def log_error(self, error_func, message, ex): #pragma: no cover
        if ex:
            error_func(message, exc_info=True)
        else:
            error_func(message)

    def report_error_to_slack(self, message):
        message = ('Error in build of image "{}" on build step "{}": {}'
                   .format(Environment.get_image_name(), self.get_step_name(), message))
        Slack.send_to_slack(message)

    def run_pipeline_step(self, data):
        if not self.step_environment_ok():
            return data
        if not self.step_data_is_ok(data):
            return data
        self.log.debug('Running "%s"', self.get_step_name())
        self.run_step(data)
        if self.next_step:
            self.next_step.run_pipeline_step(data)
        return data

    def set_next_step(self, next_step):
        self.next_step = next_step
        return next_step
