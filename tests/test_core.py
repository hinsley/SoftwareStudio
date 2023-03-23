# Import the pytest module
import pytest

# Import the core module from the softwarestudio package
from softwarestudio import core

# Define a test function that checks if the SoftwareProject class works as expected
def test_software_project():
    # Create a new project object with a name and a description
    project = core.SoftwareProject("TestProject", "A project for testing purposes")

    # Assert that the project has the correct attributes
    assert project.name == "TestProject"
    assert project.description == "A project for testing purposes"
    assert project.files == {}

    # Add a file to the project with a name and content
    project.add_file("test.txt", "This is a test file")

    # Assert that the file is added to the project files dictionary
    assert project.files == {"test.txt": "This is a test file"}

    # Generate a file for the project using GPT based on a prompt (using mock response)
    prompt = "Write a Python script that prints hello world"
    code = "print('Hello world')"
    with unittest.mock.patch("softwarestudio.gpt.generate_code", return_value=code):
        project.generate_file("hello.py", prompt)

    # Assert that the file is generated and added to the project files dictionary
    assert project.files == {"test.txt": "This is a test file", "hello.py": code}
