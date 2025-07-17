import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir

    # if have directory join the paths togheter
    if file_path:
        target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    # validate it stays within the working directory boundaries
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    # validate is it a file
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_dir, "r") as f:
            file_content = f.read(MAX_CHARS)
            if not len(file_content) <= MAX_CHARS:
                return file_content + f'...File "{file_path}" truncated at 1000 characters'
            return file_content
        
    except Exception as e:
        return f"Error accesing file: {e}"