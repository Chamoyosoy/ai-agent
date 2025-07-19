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
        # create a list with the command wanted to run 
        commands = ["python3", abs_file_path]
        if args: #if extra arguments passed add to the end of list
            commands.extend(args)

        # run a process with the arguments of commands 
        process = subprocess.run(
            commands,
            cwd=abs_working_dir, # limit the working directory 
            capture_output=True, # allow save stdout and stderr outputs
            timeout=30, #limit the execution time to 30 seconds
            text=True, # stdout and stderr are opened in text mode
            )
        
        output = []

        if process.stdout: # if stdout exist add to output 
            output.append(f'STDOUT:\n{process.stdout}')
        if process.stderr: # if sterr exist add to output 
            output.append(f'STDERR:\n{process.stderr}')

        # if return code is not 0, add the code returned to output
        if process.returncode != 0: 
            output.append(f'Process exited with code {process.returncode}')
        # return the output only if a output exits
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"