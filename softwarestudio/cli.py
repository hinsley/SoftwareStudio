# Import the argparse module
import argparse

# Import the core and gpt4 modules from the softwarestudio package
from .core import SoftwareProject
from .gpt4 import generate_code

# Import the helper functions from the helpers module
from .helpers import get_valid_file_name

# Define a function that creates a new project using GPT-4 based on user inputs
def create_project():
    # Create an argument parser object
    parser = argparse.ArgumentParser(description="Create a new software project using GPT-4")

    # Add an argument for the project name
    parser.add_argument("name", help="The name of the project")

    # Add an argument for the project description (optional)
    parser.add_argument("-d", "--description", help="The description of the project", default="")

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Create a new project object with the given name and description
    project = SoftwareProject(args.name, args.description)

    # Print a welcome message and instructions
    print(f"Welcome to SoftwareStudio {args.name}!")
    print("You can use GPT-4 to generate files for your project based on your prompts.")
    print("To exit, enter 'q' or 'quit' at any time.")

    # Loop until the user exits
    while True:
        # Ask the user for a prompt for GPT-4 to write code
        prompt = input("Enter a prompt for GPT-4 to write code: ")

        # Check if the user wants to exit
        if prompt.lower() in ("q", "quit"):
            break
        
        # Otherwise, generate code using GPT-4 based on the prompt
        code = generate_code(prompt)

        # Print the generated code
        print("GPT-4 generated code:")
        print(code)

        # Ask the user if they want to save the code as a file in their project
        save = input("Do you want to save this code as a file in your project? (y/n): ")

        # Check if the user wants to save the code as a file in their project
        if save.lower() == "y":
            # Ask the user for a valid file name for their code (using helper function)
            file_name = get_valid_file_name("Enter a file name for your code: ")

            # Add the file to their project with the given name and content (using core module method)
            project.add_file(file_name, code)

            # Print a confirmation message 
            print(f"File {file_name} added to your project.")

    
    # Save the project files to disk (using core module method)
    project.save()

    # Print a goodbye message and exit 
    print(f"Your project {args.name} has been saved.")
    print("Thank you for using SoftwareStudio. Goodbye!")

# Execute this function when this script is run from command line 
if __name__ == "__main__":
    create_project()