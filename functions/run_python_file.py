import os
import subprocess
from os.path import isfile
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs python file with specified file name",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file you want to run",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments you wish to provide to run the file, this is optional"
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    base_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_dir, file_path))


    valid_target_path = os.path.commonpath([base_dir, target_path]) == base_dir

    if not valid_target_path:
        return f'Error: Cannot execute {file_path} as it is outside the working directory'
    
    if not isfile(file_path):
        return f'Error writing cannot write to directory'

    if not file_path.endswith(".py"):
        return f'Error: {file_path} is not a python file'


    command = ["python3", target_path]
    if args: # if additional args were provided add them to the command list. use extend() method
        command.extend(args)


    try:    
    #subprocess.run allows python to execute external commands and interact with them
        result = subprocess.run(command, capture_output=True, text=True, timeout=30) # text=True simply decodes the output to string instead of raw bytes
        output_str = f"Process exited with {result.returncode}"
        if not result.stdout and not result.stderr:
            output_str += ": No output produced"
        elif result.stdout and not result.stderr:
            output_str += f": STDOUT:{result.stdout}"
        elif result.stderr and not result.stdout:
            output_str += f": STDERR{result.stderr}"
        else:
            output_str += f": STDOUT:{result.stdout}, STDERR:{result.stderr}"

    except Exception as e:
        return f"Error: executing python file: {e}"


    return output_str




