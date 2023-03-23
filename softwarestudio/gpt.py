from .config import config

# Import the OpenAI Python SDK and set the API key
import openai
openai.api_key = config["OpenAI Key"]

# Define a function that takes a user prompt and returns GPT generated code
def generate_code(prompt):
    # Make a request to the GPT API
    result = openai.Completion.create(
        model = config["Models"]["Code"], # Specify the model name
        prompt = prompt, # Specify the prompt
        max_tokens = 1000, # Specify the maximum number of tokens to generate
        temperature = 0 # Specify the temperature
    )
    # Return the content of the GPT generated message
    return result["choices"][0]["text"] # TODO: Anticipate different "finish_reason"s.

# Define a function that summarizes the contents of a file.
def document_file(filename):
    # Read the contents of the file
    with open(filename, "r") as f:
        content = f.read()
    # Make a request to the GPT API
    result = openai.ChatCompletion.create(
        model = config["Models"]["Documentation"], # Specify the model name
        messages = [
            {
                "role": "system",
                "content": f"Provide informative, concise documentation for the following file `{filename}` in Markdown format."
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    # Return the content of the GPT generated message
    return result["choices"][0]["message"]["content"]
