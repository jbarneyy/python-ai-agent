# Imports Python’s built-in os module. Used here to access environment variables (Google API key).
import os
import sys

# Imports load_dotenv() from the python-dotenv package. Will read .env file and load the environment variables into os.environ.
from dotenv import load_dotenv

# Imports the genai module from Google's SDK (google-generativeai). Access to the Client and model methods needed to talk to Gemini.
from google import genai
from google.genai import types

from functions.call_function import call_function

def main():

    if (len(sys.argv) < 2):
        print("Need to specify prompt for Gemini!")
        exit(1)

    # Reads the .env file in the root of project. Loads the variables into the environment.
    load_dotenv()

    # Retrieves the value of GEMINI_API_KEY from the environment.
    api_key = os.environ.get("GEMINI_API_KEY")

    # Creates a Client instance to interact with Google Gemini.
    client = genai.Client(api_key=api_key)

    # Grabs second value in sys.argv to be used as content to be fed to Gemini for response.
    content = sys.argv[1]

    system_prompt = """
        You are a helpful AI coding agent.
        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files
        All paths you provide should be relative to the working directory. 
        You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    
    # Creating list named messages with a single Content object. Content object includes a nested Part object with message text.
    messages = [types.Content(role="user", parts=[types.Part(text=content)])]

    # Calls Gemini’s generate_content() method using the "gemini-2.0-flash-001" model.
    response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                              contents=messages, 
                                              config=types.GenerateContentConfig(tools=[available_functions],
                                                                                 system_instruction=system_prompt))

    # Print out response's text, prompt token count, and response token count. If --verbose flag included.
    function_responses = []
    if is_verbose():
        if (response.function_calls):
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=True)
                if (not function_call_result.parts or not function_call_result.parts[0].function_response):
                    raise Exception("empty function call result")
                
                print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result)
            
            if (not function_responses):
                raise Exception("No function responses generated. Exiting")

        print(response.text)
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        if (response.function_calls):
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if (not function_call_result.parts or not function_call_result.parts[0].function_response):
                    raise Exception("empty function call result")
                
                function_responses.append(function_call_result)

            if (not function_responses):
                raise Exception("No function responses generated. Exiting")    

        print(response.text)


def is_verbose():
    if (len(sys.argv) > 2):
        return sys.argv[2] == "--verbose"
    else:
        return False


# Summary of our get_files_info function that we can pass to LLM with descriptors.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# Summary of our get_file_content function that we can pass to LLM with descriptors.
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file, returns a string containing all of a file's text, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that we will be returning the contents of, relative to the working directory.",
            ),
        },
    ),
)

# Summary of our run_python function that we can pass to LLM with descriptors.
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that we will be executing, relative to the working directory.",
            ),
        },
    ),
)

# Summary of our write_file function that we can pass to LLM with descriptors.
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file, if file does not exist will create a file. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that we will be writing, overwriting, or creating. Relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content, message, or text that we will be writing to the designated file.")
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


# Entry point for our main function.
main()