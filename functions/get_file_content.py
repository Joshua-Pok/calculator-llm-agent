import os
from os.path import isfile
from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets content of a file in specified relative directory to working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory to the file you wish to get contents for"
            )
        }
    )
)
def get_file_content(working_directory, file_path):
    base_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_dir, file_path))



    valid_target_dir = os.path.commonpath([base_dir, target_path]) == base_dir
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path} as it is outside the path permitted'

    if not isfile(file_path):
        return f'Error: {file_path} is not a file'


    with open(target_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'


    return file_content_string
        
