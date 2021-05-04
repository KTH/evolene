__author__ = 'tinglev'

import re
from modules.util import environment

def is_main_branch():
    
    branch = environment.get_git_branch()
    
    if 'master' in branch:
        return True
    
    if 'main' in branch:
        return True

    return False


def get_commit_clamped(length=7):
    
    commit_hash = environment.get_git_commit()

    if len(str(commit_hash)) > length:
        commit_hash = commit_hash[:length]
    
    return commit_hash



def slugify_branch():
    """
    Take some name (any string) and return a version-slug-safe variant of it.
    """
    # This could be done better with an external dependency,
    # but branch-names are probably ascii anyway.
    # "feature/slånbärsöl" will become "feature.sl.nb.rs.l", so it errs on the safe side.
    # If the result is an empty string, substitute "unknown"
    return re.sub('[^a-z0-9]+', '.', environment.get_git_branch().lower()).strip('.') or 'unknown'
