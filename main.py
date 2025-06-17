# Imports Python’s built-in os module. Used here to access environment variables (Google API key).
import os
import sys

# Imports load_dotenv() from the python-dotenv package. Will read .env file and load the environment variables into os.environ.
from dotenv import load_dotenv

# Imports the genai module from Google's SDK (google-generativeai). Access to the Client and model methods needed to talk to Gemini.
from google import genai
from google.genai import types

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

    # Creating list named messages with a single Content object. Content object includes a nested Part object with message text.
    messages = [types.Content(role="user", parts=[types.Part(text=content)])]

    # Calls Gemini’s generate_content() method using the "gemini-2.0-flash-001" model.
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

    # Print out response's text, prompt token count, and response token count. If --verbose flag included.
    if is_verbose():
        print(response.text)
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


def is_verbose():
    if (len(sys.argv) > 2):
        return sys.argv[2] == "--verbose"
    else:
        return False






main()