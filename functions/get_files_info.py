import os

def get_files_info(working_directory, directory=None):
    # get absolute path form a relative path
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir

    # if have directory join the paths togheter
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    # validate it stays within the working directory boundaries
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # validate is it a directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try: # try to make a sumary of every file
        files_info = []
        # for every file in the target directory do:
        for filename in os.listdir(target_dir):
            # get the filepath joining the target directory with the file name
            filepath = os.path.join(target_dir, filename)
            file_size = 0 # reset th file size every loop
            # validate if the filepath is a directory
            is_dir = os.path.isdir(filepath)
            # get th file size
            file_size = os.path.getsize(filepath)
            # add filename, size and is a directory to a list
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        # return a sigle string with line breaks
        return "\n".join(files_info)
    except Exception as e: 
        return f"Error listing files: {e}"
