import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    # get absolute path form a relative path
    abs_working_dir = os.path.abspath(working_directory)
    # join the paths togheter
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
    # validate it stays within the working directory boundaries
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    # validate is it a file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        # open the file as a file
        with open(abs_file_path, "r") as f:
            # save with a limit of chars
            file_content = f.read(MAX_CHARS)
            # if the file has more than the limit add a str indicated at the end
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        # return the file content as a text with the limit
        return file_content
    # if something goes wrong return a error
    except Exception as e:
        return f"Error accesing file: {e}"