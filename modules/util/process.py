__author__ = 'tinglev'

import subprocess
import logging
import sys
from modules.util.exceptions import PipelineException

def run_with_output(cmd, log_cmd=True):
    log = logging.getLogger(__name__)
    try:
        if log_cmd:
            log.info("Command: '%s'", cmd)

        result = subprocess.run(args = ["/bin/bash", "-i", "-c", cmd],
                    capture_output=True,
                    encoding='utf-8')

        if result:
            if result.stdout:
                return result.stdout
            if result.stderr:
                return result.stderr
            
    except subprocess.CalledProcessError as cpe:
        raise PipelineException(f'Error running command. {cpe}')
    except:
        raise PipelineException(f'Unhandled exception. {sys.exc_info()[0]}')
