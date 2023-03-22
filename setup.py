# Import the setuptools module
import setuptools

# Read the README.md file and store it as a long description
with open("README.md", "r") as f:
    long_description = f.read()

# Call the setup function to define your project
setuptools.setup(
    name="SoftwareStudio", # The name of your project
    version="0.1.0", # The version of your project
    description="A Python package that leverages GPT-4 to help developers write software without writing even a single line of code manually.", # A short description of your project
    long_description=long_description, # A long description of your project from the README.md file
    long_description_content_type="text/markdown", # The type of the long description
    url="https://github.com/hinsley/SoftwareStudio", # The URL of your project's homepage
    author="Carter David Hinsley", # The author of your project
    author_email="carterhinsley@outlook.com", # The author's email address
    license="GNU AGPL v3", # The license of your project
    packages=setuptools.find_packages(), # The packages to include in the distribution
    install_requires=["openai"], # The dependencies of your project
    classifiers=[ # The classifiers that describe your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries"
    ],
)