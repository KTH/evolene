__author__ = 'tinglev'

from modules.util.exceptions import PipelineException

def get_patch(version):
    '''
    From "2.3.45"  latest published npm version
    return "45" to use as major.minor when se.kth.automaticPublish is true.
    Defaults to None if no patch is found in the version string.
    
    '''
    result = None

    if not version:
        raise PipelineException('No version passed to get patch from.')

    if version.count('.') == 1:
        return result

    try:
        patch_version_index = version.rfind(".") + 1
        patch_version = version[patch_version_index:]
        result = int(patch_version)
        
    except:
        raise PipelineException(f"Could not get the patch version from '{version}'.")

    return result


def get_next_patch(version):
    '''
    Incremented patch version. 1.2.3 -> 1.2.4
    Defaults to 0 if no patch is found in the version string. 1.2 -> 1.2.0
    '''
    patch = get_patch(version)
    if patch is None:
        return 0

    return patch + 1


def get_major_minor(version):
    '''
    Gets the major minor didgits = "[1.2].3"
    '''
    if not version:
        raise PipelineException('No version passed to get major.minor from.')

    if version.count('.') == 1:
        return version

    patch_version_index = version.rfind(".")
    result = version[:patch_version_index]

    return result


def get_next(version):
    '''
    Gets the next version 
    major.minor.[patch +1]
    '''
    major_minor = get_major_minor(version)
    patch = get_next_patch(version)
    next_version = f"{major_minor}.{patch}"

    return next_version