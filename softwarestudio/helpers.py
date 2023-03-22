import os

# Define a function that checks if a file name is valid
def is_valid_file_name(name):
    # Check if the name is empty or contains invalid characters
    if not name or any(c in name for c in r'\/:*?"<>|'):
        return False
    
    # Check if the name is too long
    if len(name) > 255:
        return False
    
    # Check if the name already exists in the current directory
    if os.path.exists(name):
        return False
    
    # Otherwise, return True
    return True

# Define a function that validates a user input for a file name
def get_valid_file_name(prompt):
    # Loop until a valid file name is entered
    while True:
        # Ask the user for a file name
        name = input(prompt)

        # Check if the file name is valid
        if is_valid_file_name(name):
            # Return the file name
            return name
        
        # Otherwise, print an error message and repeat
        else:
            print("Invalid file name. Please try again.")
