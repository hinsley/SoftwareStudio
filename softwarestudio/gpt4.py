# Import the openai package and set the API key
import openai
openai.api_key = "YOUR_KEY"

# Define a function that takes a user prompt and returns GPT-4 generated code
def generate_code(prompt):
    # Set the system intelligence parameter to tell GPT-4 to write code as an expert
    system_intel = "You are GPT-4, write Python code as if you were an expert in the field."
    # Make a request to the GPT-4 API using the ChatCompletion endpoint
    result = openai.ChatCompletion.create(
        model="gpt-4", # Specify the model name
        messages = [ # Provide the messages for the chat
            {
                "role": "system", # The role of the system
                "content": system_intel # The content of the system message
            },
            {
                "role": "user", # The role of the user
                "content": prompt # The content of the user message (the prompt)
            }
        ]
    )
    # Return the content of the GPT-4 generated message
    return result["choices"][0]["message"]["content"]
