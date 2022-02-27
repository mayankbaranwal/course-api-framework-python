import json
from pathlib import Path
# Making use of pathlib ensure that all the paths that you create are cross-platform and can work very easily.

BASE_PATH = Path.cwd().joinpath('..', 'tests', 'data')


def read_file(file_name):
    path = get_file_with_json_extension(file_name)
    # using path.open() instead of direct method open(), this is very useful pattern because it ensures that open() is
    # able to understand the file path quite easily. Also, finally when we get a handle to the file in 'f', we're making
    # use of json.load() because we want to read directly from this file and then return a python object.
    #
    with path.open(mode='r') as f:
        return json.load(f)


def get_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = BASE_PATH.joinpath(file_name)
    else:
        path = BASE_PATH.joinpath(f'{file_name}.json')
    return path
