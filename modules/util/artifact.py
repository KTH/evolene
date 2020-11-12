__author__ = 'tinglev'

from modules.util import environment
from modules.util import git

def branch_starts_with(pattern):
    return environment.get_git_branch().startswith(pattern)

def should_store():
    '''
    Should the artifact (npm packqge, docker image...) built be store in some repository somewhere?
    '''
    if git.is_main_branch():
        return True

    if branch_starts_with(environment.get_also_push_branches_starting_with()):
        return True

    return False
    