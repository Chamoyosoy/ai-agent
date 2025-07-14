import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    model='gemini-2.0-flash-001', contents=prompt
    )

    print("Response: ")
    print(response.text)


    if verbose:
        metadata = response.usage_metadata
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

if __name__ == "__main__":
    main()

