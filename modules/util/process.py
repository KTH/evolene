__author__ = 'tinglev'

import subprocess
import logging
import sys
from modules.util.exceptions import PipelineException

def run_with_output(cmd, log_cmd=False, check=False):
    log = logging.getLogger("-")
    try:
        if log_cmd:
            log.info("Command: '%s'", cmd)

        result = subprocess.run(args = ["/bin/bash", "-i", "-c", cmd],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=check,
                    encoding='utf-8')

        if result:
            return result.stdout
            
    except subprocess.CalledProcessError as cpe:
        log.info(str(cpe))
        raise PipelineException(f'{cpe.output}')
    except:
        raise PipelineException(f'Unhandled exception when execution command.')
