import os
from pathlib import Path
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    # directory parameter is relative to working directory,
    # but working directory is defined by us so we can scope the files the LLM can view
    
    base_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(base_dir, directory))


    valid_target_dir = os.path.commonpath([base_dir, target_dir]) == base_dir
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # returning string errors allow the LLM to handle errors gracefully


    path = Path(target_dir)
    if not path.exists():
        return f'Error: {directory} does not exist'
    if not path.is_dir():
        return f'Error: {directory} is not a directory'


    lines = []
    for item in path.iterdir():
        try:
            size = item.stat().st_size if item.is_file() else 0
            output_str = f"- {item.name}: file_size={item.__sizeof__()}bytes, is_dir={item.is_dir()}"
            print(output_str)

        except OSError:
            size = 0

        lines.append(f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}")


    return "\n".join(lines) if lines else "(empty directory)"


