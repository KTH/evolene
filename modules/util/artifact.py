__author__ = 'tinglev'

import logging
from modules.util import environment
from modules.util import git

log = logging.getLogger("-")


def branch_starts_with(pattern):
    if not pattern:
        log.debug('No pattern passed.')
        return False

    result = str(environment.get_git_branch()).startswith(pattern)

    log.debug(f'Branch starts with {pattern}.')

    return result


def should_store():
    '''
    Should the artifact (npm packqge, docker image...) built be store in some repository somewhere?
    '''
    if git.is_main_branch():
        log.info(
            f'Built artefact will be stored in repository since it is {environment.get_git_branch()}.')
        return True

    if branch_starts_with(environment.get_branches_save_starting_with()):
        log.info(f'Branch {environment.get_git_branch()} is not main/master but is configured to be stored anyway, according to BRANCHES_SAVE_STARTING_WITH: {environment.get_branches_save_starting_with()}')
        return True

    log.info(
        f'Built artefact will not be stored in any repository, it is in a branch {environment.get_git_branch()}.')

    return False
