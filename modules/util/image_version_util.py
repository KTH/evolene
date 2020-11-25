__author__ = 'tinglev'

import re
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import pipeline_data

def is_major_minor_patch(image_version):
    if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', image_version):
        return False
    return True

def is_major_minor_only(image_version):
    if not re.match(r'^[0-9]+\.[0-9]+$', image_version):
        return False
    return True

def get_image(data):
    if data[pipeline_data.IMAGE_NAME] is None:
        raise PipelineException("Missing the name of the image.")
    if data[pipeline_data.IMAGE_VERSION] is None:
        raise PipelineException("Missing the version for the image.")
    return '{}:{}'.format(data[pipeline_data.IMAGE_NAME], data[pipeline_data.IMAGE_VERSION])

def get_image_only_semver(data):
    if data[pipeline_data.IMAGE_NAME] is None:
        raise PipelineException("Missing the name of the image.")
    if data[pipeline_data.SEM_VER] is None:
        raise PipelineException("Missing the SemVer for the image.")
    return '{}:{}'.format(data[pipeline_data.IMAGE_NAME], data[pipeline_data.SEM_VER])

def get_latest_tag(data):
    return '{}:{}'.format(data[pipeline_data.IMAGE_NAME], 'latest')

def prepend_registry(image):
    return '{}/{}'.format(environment.get_registry_host(), image)
