# Import the gpt4 module
from .gpt4 import generate_code

# Define a class that represents a software project
class SoftwareProject:
    # Initialize the project with a name and a description
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.files = {} # A dictionary to store the project files

    # Add a file to the project with a given name and content
    def add_file(self, name, content):
        self.files[name] = content

    # Generate a file for the project using GPT-4 based on a prompt
    def generate_file(self, name, prompt):
        content = generate_code(prompt) # Call the gpt4 module function
        self.add_file(name, content) # Add the file to the project

    # Save the project files to disk
    def save(self):
        # Create a directory for the project if it does not exist
        import os
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        
        # Write each file to disk in the project directory
        for name, content in self.files.items():
            with open(os.path.join(self.name, name), "w") as f:
                f.write(content)

# Define a function that creates a sample project for demonstration purposes
def create_sample_project():
    # Create a new project with a name and a description
    project = SoftwareProject("HelloWorld", "A simple Python program that prints hello world")

    # Generate a file for the project using GPT-4 based on a prompt
    prompt = "Write a Python script that prints hello world"
    project.generate_file("hello.py", prompt)

    # Save the project files to disk
    project.save()

    # Return the project object
    return project
