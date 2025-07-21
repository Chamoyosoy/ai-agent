import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    # loads environment variables from a .env
    load_dotenv()

    # check if --verbose is use
    verbose = "--verbose" in sys.argv
    # save system args if not have "--" flag
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    # check and teach te correct usage
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    # join the prompt in a sigle str cause normally is saved as a list of words(strs)
    user_prompt = " ".join(args)

    # save the apikey and the chosed client to use
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {user_prompt}")

    prompt=[
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    generate(client, prompt, verbose)


def generate(client, prompt, verbose):

    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=prompt,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # if not function is calling return only a response
    if not response.function_calls:
        return response.text

    # to all function calling print the function retrun
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    if verbose:
        metadata = response.usage_metadata
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

if __name__ == "__main__":
    main()

