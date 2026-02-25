import os
from os.path import isfile

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)


    valid_target_dir = os.path.commonpath([abs_path, file_path]) == abs_path
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path} as it is outside the path permitted"'

    if not isfile(file_path):
        return f'Error: {file_path} is not a file'


    with open(file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
