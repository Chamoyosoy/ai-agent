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
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        process = subprocess.run(['python3', abs_file_path], cwd=abs_working_dir, capture_output=True, timeout=30)
        print(f'STDOUT: {process.stdout.decode("utf-8")}')
        print(f'STDERR: {process.stderr.decode("utf-8")}')
        if not process.returncode == None:
            return f'Process exited with code "{process.returncode}"'
        if process.stdout == "":
            return 'No output produced'
        
    except Exception as e:
        return f"Error: executing Python file: {e}"