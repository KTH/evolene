__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import slack

class CelebrateStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [environment.BUILD_NUMBER]

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_NAME]

    def run_step(self, data):
        self.do_we_have_a_reason_to_party(data)
        return data

    def do_we_have_a_reason_to_party(self, data):
        message = self.get_party_message(data)
        if message:
            slack.send(self.get_party_message(data), icon=":parrot_party:")

    def get_party_message(self, data):
        build_nr = int(str(environment.get_build_number()))
        if build_nr % 100 == 0:
            return ("<!here> :parrot_party: :parrot_party: :parrot_party: {} build number {}! "
                    "You are worth some :champagne:\nhttps://www.youtube.com/watch?v=eCzhNPSXpfI"
                    .format(data[pipeline_data.IMAGE_NAME], build_nr))
        return None
