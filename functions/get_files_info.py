import os

def get_files_info(working_directory, directory=None):

    working_dir_path = os.path.abspath(working_directory)

    if (directory):
        dir_path = os.path.join(working_dir_path, directory)
        dir_path = os.path.abspath(dir_path)

    # print(working_dir_path)
    # print(dir_path)

    if (not dir_path.startswith(working_dir_path)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if (not os.path.isdir(dir_path)):
        return f'Error: "{directory}" is not a directory'

    dir_contents = os.listdir(dir_path)
    # print(dir_contents)

    dir_item_info = []

    for item in dir_contents:
        item_path = os.path.join(dir_path, item)
        # print(item_path)

        dir_item_info.append(
            f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
        )
    
    # print(dir_item_info)


    return "\n".join(dir_item_info)
