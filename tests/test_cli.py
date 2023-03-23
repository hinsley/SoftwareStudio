import pytest

# Import the cli module from the softwarestudio package
from softwarestudio import cli

# Define a test function that checks if the create_project function works as expected
def test_create_project():
    # Define some sample arguments and expected outputs
    args = [
        ["TestProject"],
        ["TestProject", "-d", "A project for testing purposes"]
    ]

    outputs = [
        "Welcome to SoftwareStudio TestProject!\nYou can use GPT to generate files for your project based on your prompts.\nTo exit, enter 'q' or 'quit' at any time.",
        "Welcome to SoftwareStudio TestProject!\nYou can use GPT to generate files for your project based on your prompts.\nTo exit, enter 'q' or 'quit' at any time."
    ]

    # Loop through each argument and output pair
    for arg, output in zip(args, outputs):
        # Mock the sys.argv attribute to use the argument as command line input
        with unittest.mock.patch("sys.argv", ["cli.py"] + arg):
            # Mock the input function to return 'q' as user input to exit the loop
            with unittest.mock.patch("builtins.input", return_value="q"):
                # Mock the print function to capture the output of the create_project function
                with unittest.mock.patch("builtins.print") as mock_print:
                    # Call the create_project function 
                    cli.create_project()

                    # Assert that the print function was called with the expected output as first argument
                    mock_print.assert_called_with(output)
