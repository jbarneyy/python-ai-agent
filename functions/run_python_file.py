import os
import subprocess


def run_python_file(working_directory, file_path):

    working_dir_path = os.path.abspath(working_directory)
    file_path_cp = os.path.abspath(os.path.join(working_dir_path, file_path))

    # print(working_dir_path)
    # print(file_path_cp)

    if (not file_path_cp.startswith(working_dir_path)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if (not os.path.exists(file_path_cp)):
        return f'Error: File "{file_path}" not found.'
    
    if (os.path.basename(file_path_cp)[-3:] != ".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        run_file = subprocess.run(["python", os.path.basename(file_path_cp)],
                       timeout=30,
                       capture_output=True,
                       text=True,
                       cwd=os.path.dirname(file_path_cp))
        
        if (run_file.stdout == "" and run_file.stderr == ""):
            return "No output produced."

        return_string = ""

        return_string += f"STDOUT: {run_file.stdout}"
        return_string += f"\nSTDERR: {run_file.stderr}"

        if (run_file.returncode != 0):
            return_string += f"\nProcess exited with code {run_file.returncode}"

        return return_string

        

    except Exception as e:
        return f"Error: executing Python file {file_path}: {e}"
    
