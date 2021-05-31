__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import print_util

class SetupStep(AbstractPipelineStep):

    name = "Setup pipeline steps"

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        self.print_header()
        self.step_ok()
        return data

    def print_header(self):
        print_util.black("                                                    ")
        print_util.pink("  ______                   _                         ")
        print_util.pink(" |  ____|                 | |                        ")
        print_util.pink(" | |__    __   __   ___   | |   ___   _ __     ___   ")
        print_util.pink(" |  __|   \ \ / /  / _ \  | |  / _ \ | '_ \   / _ \  ")
        print_util.pink(" | |____   \ V /  | (_) | | | |  __/ | | | | |  __/  ")
        print_util.pink(" |______|   \_/    \___/  |_|  \___| |_| |_|  \___|  ")
        print_util.black("                                                    ")
        print_util.black("                                                    ")
        print_util.black("****************************************************")
        print_util.black(" Help make Evolene better!                          ")
        print_util.black(" https://github.com/kth/evolene                     ")
        print_util.black("****************************************************")
        print_util.black("                                                    ")
