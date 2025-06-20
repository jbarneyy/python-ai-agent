from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

from google.genai import types


def call_function(function_call_part: types.FunctionCall, verbose=False):

    function_name = function_call_part.name
    function_args = function_call_part.args
    function_result = None

    if (verbose):
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_args["working_directory"] = "./calculator"

    if (function_name == "get_files_info"):
        # function_result = get_files_info(**function_args)
        function_result = get_files_info(function_args["working_directory"], function_args["directory"])
    elif (function_name == "get_file_content"):
        # function_result = get_file_content(**function_args)
        function_result = get_file_content(function_args["working_directory"], function_args["file_path"])
    elif (function_name == "run_python_file"):
        # function_result = run_python_file(**function_args)
        function_result = run_python_file(function_args["working_directory"], function_args["file_path"])
    elif (function_name == "write_file"):
        # function_result = write_file(**function_args)
        function_result = write_file(function_args["working_directory"], function_args["file_path"], function_args["content"])
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    