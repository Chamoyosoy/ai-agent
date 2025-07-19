import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    # get absolute path form a relative path
    abs_working_dir = os.path.abspath(working_directory)
    # join the paths togheter
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # validate it stays within the working directory boundaries
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # validate if exist the file
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    # validate if the file is a python file
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python3", abs_file_path]
        if args:
            commands.extend(args)

        process = subprocess.run(
            commands,
            cwd=abs_working_dir,
            capture_output=True,
            timeout=30,
            text=True,
            )
        
        output = []

        if process.stdout:
            output.append(f'STDOUT:\n{process.stdout}')
        if process.stderr:
            output.append(f'STDERR:\n{process.stderr}')


        if process.returncode != 0:
            output.append(f'Process exited with code {process.returncode}')
        
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"