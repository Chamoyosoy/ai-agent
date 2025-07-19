import os

def write_file(working_directory, file_path, content):
     # get absolute path form a relative path
    abs_working_dir = os.path.abspath(working_directory)
    # join the paths togheter
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # validate it stays within the working directory boundaries
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # validate if exist the directory where th file is
    if not os.path.exists(abs_file_path):
        try: #if not exist try to create the path 
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            # print(f"file not found, create a new file in {os.path.dirname(abs_file_path)}")
        except Exception as e:
            return f'Error: creating directory {e}'
    # validate if is a file or a directory
    if os.path.exists(abs_working_dir) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    # write the file with the content
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        # return which file was wrote and the numbers of characters
        return f'Succesfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing to file "{e}"' 