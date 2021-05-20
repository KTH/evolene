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
        if result and result.stdout:
            return result.stdout

            
    except subprocess.CalledProcessError as cpe:
        if cpe.output:
            raise PipelineException(cpe.output.decode('utf-8'))
        raise PipelineException(f"{str(cpe)}")
    except:
        raise PipelineException(
            "Unabled exception. {}".format(sys.exc_info()[0]))

