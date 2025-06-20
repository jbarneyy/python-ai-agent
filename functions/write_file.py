import os


def write_file(working_directory, file_path, content):

    working_dir_path = os.path.abspath(working_directory)
    file_path_cp = os.path.abspath(os.path.join(working_dir_path, file_path))

    # print(working_dir_path)
    # print(file_path_cp)

    if (not file_path_cp.startswith(working_dir_path)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if (not os.path.exists(os.path.dirname(file_path_cp))):

            os.makedirs(os.path.dirname(file_path_cp))

            with open(file_path_cp, "w") as file:
                file.write(content)
        
        else:
            with open(file_path_cp, "w") as file:
                file.write(content)
        
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        

    except Exception as e:
        return f'Error with file {file_path}: {e}'

