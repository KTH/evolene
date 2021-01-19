__author__ = 'tinglev'
import re

def clean(text):
    error = str(text)
    error = remove_possible_npm_standard_msg(error)
    error = remove_possible_ansi_colors(error)
    error = remove_docker_compose_output(error)
    return str(error).replace('`', ' ')[-1000:]

def remove_possible_npm_standard_msg(error):
    '''
    When system exiting is not 0, npm adds crap to the output. We remove this.

    npm ERR! code ELIFECYCLE
    npm ERR! errno 1
    npm ERR! kth-azure-app@0.1.0 test-integration: ./tests/integration-tests/basic.sh`
    npm ERR! Exit status 1
    npm ERR!
    npm ERR! Failed at the kth-azure-app@0.1.0 test-integration script.
    npm ERR! This is
    '''

    return error[:error.find("npm ERR!")]

def remove_possible_ansi_colors(error):
    '''
    When output is done in terminal with ANSI colors (like [0m    [0;0m'),
    texts get harder to read, we remove this encoding.

    [33mintegration-tests_1_193822f6013a |[0m    [0;0m'http://web/' does not contain pattern 'user'.
    [33mintegration-tests_1_193822f6013a |[0m
    '''
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
        ''', re.VERBOSE)
        
    return ansi_escape.sub('', error)

def remove_docker_compose_output(error):
    '''
    Running tests in Docker Compse adds extra container info we dont need to see.

    web_1_1b99cff96784 |   1 passing (473ms)
    web_1_1b99cff96784 |   1 failing

    '''
    text_matcher = re.compile(r"[^\s]+ \|+ ", flags=re.MULTILINE)

    return text_matcher.sub('', error)
