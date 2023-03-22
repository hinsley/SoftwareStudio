import pytest

# Import the helpers module from the softwarestudio package
from softwarestudio import helpers

# Define a test function that checks if the is_valid_file_name function works as expected
def test_is_valid_file_name():
    # Define some sample file names and expected results
    file_names = [
        "test.txt",
        "hello.py",
        "",
        "foo/bar",
        "test*txt",
        "a" * 256
    ]

    results = [
        True,
        True,
        False,
        False,
        False,
        False
    ]

    # Loop through each file name and result pair
    for file_name, result in zip(file_names, results):
        # Call the is_valid_file_name function with the file name and assert that it returns the result
        assert helpers.is_valid_file_name(file_name) == result
