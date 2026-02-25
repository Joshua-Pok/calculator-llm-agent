import os
from pathlib import Path
from os.path import isdir

def write_file(working_directory, file_path, content):


    base_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_dir, file_path))


    valid_target_path = os.path.commonpath([base_dir, target_path]) == base_dir
    
    if not valid_target_path: 
        return f'Error: cannot write to {file_path} as it is outside working directoty'


    if isdir(file_path):
        return f'Error: Cannot write to {file_path} as it is a directory'


    with open(target_path, "w") as f:
        try:
            f.write(content)
            return f'Successfully wrote to {file_path} ({len(content)} characters written)'
        except Exception as e:
            return f'Error writing to file: {e}'
