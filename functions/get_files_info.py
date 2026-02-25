import os
from pathlib import Path


def get_files__info(working_directory, directory="."):
    # directory parameter is relative to working directory,
    # but working directory is defined by us so we can scope the files the LLM can view
    
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.join(abs_path, directory)
    normalized_full_path = os.path.normpath(full_path)


    valid_target_dir = os.path.commonpath([abs_path, normalized_full_path]) == abs_path
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # returning string errors allow the LLM to handle errors gracefully


    path = Path(normalized_full_path)
    for item in path.iterdir():
        output_str = f"- {item.name}: file_size={item.__sizeof__()}bytes, is_dir={item.is_dir()}"
        print(output_str)


