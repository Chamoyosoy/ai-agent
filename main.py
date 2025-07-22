import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS

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

    # select the apikey and then chosed client to use
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # if --verbose is passed print the user prompt a the begining
    if verbose:
        print(f"User prompt: {user_prompt}")

    # pass the prompt as the client need 
    prompt=[
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # call generate funtion which is the function to generate content and call funcs
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f'Maximum iterations ({MAX_ITERS}) reached')
            sys.exit(1)
        try:
            final_response = generate(client, prompt, verbose)
            if final_response:
                print("final response:")
                print(final_response)
                break
        except Exception as e:
            print(f'Error in generate content: {e}')


def generate(client, prompt, verbose):
    # generate the response with some alligment
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', #select th model who use
    contents=prompt, # pass the menssge from the user
    config=types.GenerateContentConfig( # pass the available functions to use and a firts instruction prompt, saved in "prompts.py"
    tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            prompt.append(function_call_content)

    # if not functions are called return only a response
    if not response.function_calls:
        return response.text

    # when func is needed call it and save in a list 
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])


    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    prompt.append(types.Content(role="tool", parts=function_responses))
    # if -- verbose was pass print metadata from response
    if verbose:
        metadata = response.usage_metadata
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")


if __name__ == "__main__":
    main()