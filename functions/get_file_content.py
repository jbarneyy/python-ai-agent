import os

def get_file_content(working_directory, file_path):

    working_dir_path = os.path.abspath(working_directory)
    file_path_cp = os.path.abspath(os.path.join(working_dir_path, file_path))

    # print(working_dir_path)
    # print(file_path_cp)

    if (not file_path_cp.startswith(working_dir_path)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if (not os.path.isfile(file_path_cp)):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10_000

    try:
        with open(file_path_cp, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if (len(file_content_string) == MAX_CHARS):
            file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    
    except Exception as e:
        
        return f'Error reading file "{file_path}": {e}'