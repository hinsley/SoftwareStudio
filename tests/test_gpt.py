import pytest

# Import the gpt module from the softwarestudio package
from softwarestudio import gpt

# Define a test function that checks if the generate_code function works as expected
def test_generate_code():
    # Define some sample prompts and expected responses (using mock responses)
    prompts = [
        "Write a Python script that prints hello world",
        "Write a Python function that returns the sum of two numbers",
        "Write a Python class that represents a person with a name and an age"
    ]
    
    responses = [ # TODO: These need to be changed. I haven't actually checked what the seed used produces for these outputs. But this should give an idea of what I'm expecting.
        "print('Hello world')",
        "def add(x, y):\n\treturn x + y",
        "class Person:\n\tdef __init__(self, name, age):\n\t\tself.name = name\n\t\tself.age = age"
    ]

    # Loop through each prompt and response pair
    for prompt, response in zip(prompts, responses):
        # Mock the openai.ChatCompletion.create method to return the response as GPT generated message
        with unittest.mock.patch("openai.ChatCompletion.create", return_value={"choices": [{"message": {"content": response}}]}, seed=0):
            # Call the generate_code function with the prompt and assert that it returns the response
            assert gpt.generate_code(prompt) == response
