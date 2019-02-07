__author__ = 'tinglev'

import unittest
from modules.pipeline_steps.instruction_step import InstructionStep
from modules.util.data import Data

class InstructionStepTests(unittest.TestCase):

    def test_is_instruction_entrypoint(self):
        self.assertTrue(InstructionStep().is_instruction_entrypoint(
            'ENTRYPOINT ["make", "main.cpp]'
        ))

    def test_is_instruction_cmd(self):
        self.assertFalse(InstructionStep().is_instruction_entrypoint(
            'CMD ["make", "main.cpp]'
        ))

    def test_is_instruction_message_on_change(self):
        data = {Data.IMAGE_NAME: 'kth-azure-app', Data.IMAGE_VERSION: '1.0.0'}
        message = InstructionStep().get_change_message('ENTRYPOINT ["make", "main.cpp]', data)
        self.assertEqual(message, '*kth-azure-app:1.0.0*: In `/Dockerfile` change `ENTRYPOINT ["make", "main.cpp]` to: ```CMD ["make", "main.cpp]```')

    def test_is_instruction_message_on_no_change(self):
        data = {Data.IMAGE_NAME: 'kth-azure-app', Data.IMAGE_VERSION: '1.0.0'}
        message = InstructionStep().get_change_message('CMD ["make", "main.cpp]', data)
        self.assertEqual(message, '*kth-azure-app:1.0.0*: In `/Dockerfile` change `CMD ["make", "main.cpp]` to: ```CMD ["make", "main.cpp]```')
