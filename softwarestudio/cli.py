import argparse
import os

# Import the core and gpt modules from the softwarestudio package
from .core import SoftwareProject
from .gpt import document_file, generate_code, generate_metadata

# Import the helper functions from the helpers module
from .helpers import get_valid_file_name

# Define a function that creates a new project using GPT based on user inputs
def create_project():
    # Create an argument parser object
    parser = argparse.ArgumentParser(description="Create a new software project using GPT")

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
    print("You can use GPT to generate files for your project based on your prompts.")
    print("To exit, enter 'q' or 'quit' at any time.")

    # Loop until the user exits
    while True:
        # Ask the user for a prompt for GPT to write code
        prompt = input(">>> ")

        # Check if the user wants to exit
        if prompt.lower() in ("q", "quit"):
            break
        elif prompt.lower().startswith("summarize "):
            documentation = document_file(os.path.join(project.name, prompt[len("summarize "):]))
            print("GPT generated documentation:")
            print(documentation)

            # Ask the user if they want to save the documentation as a file in their project
            save = input("Do you want to save this documentation as a file in your project? (y/n): ")

            # Check if the user wants to save the documentation as a file in their project
            if save.lower() == "y":
                # Ask the user for a valid file name for their documentation (using helper function)
                file_name = get_valid_file_name("Enter a file name for your documentation: ")

                # Add the file to their project with the given name and content (using core module method)
                project.add_file(file_name, documentation)
                project.save()

                # Print a confirmation message 
                print(f"File {file_name} added to your project.")
            continue
        elif prompt.lower().startswith("metadata "):
            metadata = generate_metadata(os.path.join(project.name, prompt[len("metadata "):]))
            print("GPT generated metadata:")
            print(metadata)

            # Ask the user if they want to save the metadata as a file in their project
            save = input("Do you want to save this metadata as a file in your project? (y/n): ")

            # Check if the user wants to save the metadata as a file in their project
            if save.lower() == "y":
                # Ask the user for a valid file name for their metadata (using helper function)
                file_name = get_valid_file_name("Enter a file name for your metadata: ")

                # Add the file to their project with the given name and content (using core module method)
                project.add_file(file_name, metadata)
                project.save()

                # Print a confirmation message 
                print(f"File {file_name} added to your project.")
            continue
        elif prompt.lower().startswith("ls"):
            # Get files in the project directory
            files = os.listdir(project.name)

            # Print the files
            print("Files in your project:")
            for file in files:
                print(file)
            continue
        
        # Otherwise, generate code using GPT based on the prompt
        code = generate_code(prompt)

        # Print the generated code
        print("GPT generated code:")
        print(code)

        # Ask the user if they want to save the code as a file in their project
        save = input("Do you want to save this code as a file in your project? (y/n): ")

        # Check if the user wants to save the code as a file in their project
        if save.lower() == "y":
            # Ask the user for a valid file name for their code (using helper function)
            file_name = get_valid_file_name("Enter a file name for your code: ")

            # Add the file to their project with the given name and content (using core module method)
            project.add_file(file_name, code)
            project.save()

            # Print a confirmation message 
            print(f"File {file_name} added to your project.")

    # Print a goodbye message and exit 
    print("Thank you for using SoftwareStudio. Goodbye!")

# Execute this function when this script is run from command line 
if __name__ == "__main__":
    create_project()
