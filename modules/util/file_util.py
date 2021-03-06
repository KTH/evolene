__author__ = 'tinglev'

import os
from modules.util import environment

def get_lines(relative_file_path):
    result = []
    if is_file(relative_file_path):
        with open(get_absolue_path(relative_file_path)) as afile:
            for line in afile:
                result.append(line.strip())

    return result

def read_as_string(relative_file_path):
    if is_file(relative_file_path):
        with open(get_absolue_path(relative_file_path)) as afile:
            return afile.read()
    return None

def get_absolue_path(relative_file_path):
    return '{}{}'.format(get_project_root(), relative_file_path)

def get_project_root():
    return environment.get_project_root().rstrip('/')

def is_file(relative_file_path):
    return os.path.isfile(get_absolue_path(relative_file_path))

def is_directory(relative_file_path):
    path = get_absolue_path(relative_file_path)
    return os.path.isdir(path)

def overwite(relative_file_path, content):
    print('Path write: {}'.format(get_absolue_path(relative_file_path)))

    with open(get_absolue_path(relative_file_path), 'w+') as output_file:
        output_file.write(content)
