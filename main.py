import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts.prompts import system_prompt
from functions.call_function import available_functions
from call_function import call_function

def main():
    print("Hello from llm-agent-python!")
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("No Api key found")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )


        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        fn_results_list = []

        if response.function_calls:
            for fn in response.function_calls:
                function_result = call_function(fn)
                if not function_result.parts:
                    raise RuntimeError("empty parts ")

                if not function_result.parts[0].function_response:
                    raise RuntimeError("Empty function response of first item in parts")


                if not function_result.parts[0].function_response.response:
                    raise RuntimeError("Empty response")

                fn_results_list.append(function_result.parts[0])
                print(f"Calling function: {fn.name}({fn.args})")
                if args.verbose:
                    print(f"-> {function_result.parts[0].function_response.response}")

        else:
            print(response.text)
            break

        if response.usage_metadata is None:
            raise RuntimeError("Gemini API request failed")

        if args.verbose:
            print(f"User Prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


        messages.append(types.Content(role="user", parts=fn_results_list))


    exit(1)


if __name__ == "__main__":
    main()
