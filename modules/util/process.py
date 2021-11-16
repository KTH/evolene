__author__ = 'tinglev'

import subprocess
import logging
import os
from modules.util.exceptions import PipelineException

def run_with_output(cmd, log_cmd=False, check=False):
    log = logging.getLogger("-")
    try:
        if log_cmd:
            log.info("Command: '%s'", cmd)

        os.environ["BASH_ENV"] = "~/.bashrc"
        result = subprocess.run(args = cmd,
                    shell=True,
                    executable="/bin/bash",
                    capture_output=True,
                    check=check,
                    encoding='utf-8')

        if result:
            if result.stdout:
                return result.stdout
            if result.stderr:
                return result.stderr
           
    except subprocess.CalledProcessError as cpe:
        log.info(str(cpe))
        raise PipelineException(f'{cpe.output}')
    except:
        raise PipelineException(f'Unhandled exception when execution command.')
