from .config import config

# Import the OpenAI Python SDK and set the API key
import openai
openai.api_key = config["OpenAI Key"]

# Import SHA256 hashing function
from hashlib import sha256

# Define a function that summarizes the contents of a file.
def document_file(filename):
    # Read the contents of the file
    with open(filename, "r") as f:
        content = f.read()
    # Make a request to the GPT API
    result = openai.ChatCompletion.create(
        model = config["Models"]["Documentation"], # Specify the model name
        messages = [
            {
                "role": "system",
                "content": f"Provide informative, concise documentation for the following file `{filename}` in Markdown format."
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    # Return the content of the GPT generated message
    return result["choices"][0]["message"]["content"]

# Define a function that takes a user prompt and returns GPT generated code
def generate_code(prompt):
    # Make a request to the GPT API
    result = openai.Completion.create(
        model = config["Models"]["Code"], # Specify the model name
        prompt = prompt, # Specify the prompt
        max_tokens = 1000, # Specify the maximum number of tokens to generate
        temperature = 0 # Specify the temperature
    )
    # Return the content of the GPT generated message
    return result["choices"][0]["text"] # TODO: Anticipate different "finish_reason"s.

# Define a function that takes a user prompt and returns GPT generated metadata
def generate_metadata(filename):
    # Get the file segmentation.
    segmentation = segment_file(filename)
    # Read the contents of the file
    with open(filename, "r") as f:
        lines = f.readlines()
    segments = []
    for i in range(1, len(segmentation)):
        segments.append("\n".join(lines[segmentation[i-1]-1:segmentation[i]-1]))
    segments.append("\n".join(lines[segmentation[-1]-1:])) # TODO: Can this be empty? If so, don't append it.

    # Get GPT to generate the metadata.
    metadata = ""
    for segment in segments:
        result = openai.ChatCompletion.create(
            model = config["Models"]["Metadata"], # Specify the model name
            messages = [
                {
                    "role": "system",
                    "content": f"You are to produce the content of a concise header file for the following file `{filename}` in YAML format. Do not respond to the user with anything that is not the actual YAML markup (don't explain anything, and don't tell the user what you are providing; just give the YAML)."
                },
                {
                    "role": "system",
                    "content": f"The in-progress YAML header is:\n\n{metadata}\n\n The next segment of `{filename}` for you to append details for to the YAML header file is as follows; again, ***do not explain what you have changed or added***."
                },
                {
                    "role": "user",
                    "content": segment
                }
            ]
        )
        metadata = result["choices"][0]["message"]["content"]
    # Return the content of the GPT generated message with a prepended hash of the file contents
    return f"File SHA-256 hash: {sha256(metadata.encode()).hexdigest()}\n\n{metadata}"

def segment_file(filename):
    context_length = 100 # The number of lines of the source code file to provide to GPT at a time
    # Read the contents of the file
    with open(filename, "r") as f:
        lines = f.readlines()
    for (i, line) in enumerate(lines): # Prepend line numbers to the lines
        lines[i] = f"{i + 1} | {line}"
    if lines == []: # If the file is empty, there are no segments
        return []
    segments = set([1])
    last_csv = [1]
    context_first_line = None # The first line of the current context
    while context_first_line != max(segments):
        context_first_line = last_csv[-1] # Start this context at the beginning of the last found segment
        context_last_line = context_first_line + context_length
        context = "\n".join(lines[context_first_line-1:context_last_line-1])
        # Make a request to the GPT API
        result = openai.ChatCompletion.create(
            model = config["Models"]["Segmentation"], # Specify the model name
            messages = [
                {
                    "role": "system",
                    "content": f"Produce a comma-separated list of line numbers (from the beginnings of the lines) corresponding to the beginning of the most important two definitions and imports in the following piece of a file `{filename}`. Produce only one line of CSV format data (example: 221,370,420,435,490). If there are no segments, produce the first line number of the given snippet."
                },
                {
                    "role": "user",
                    "content": context
                }
            ]
        )
        # Obtain the content of the GPT generated message
        response = result["choices"][0]["message"]["content"]

        # Do a little sanitization
        response = response.replace(".", "").replace(" ", "")
        # Check if the response is non-empty and contains only digits and commas
        if response == "" or not all(c in "0123456789," for c in response):
            if context_last_line >= len(lines): # If the context is the last context, stop trying
                break
            context_first_line = None # Don't stop trying upon next while conditional
            continue # Try again

        # Extract the comma-separated list of line numbers
        last_csv = [int(line_number) for line_number in response.split(",")]
        # Append the line numbers to the list of segment line numbers
        if last_csv == sorted(last_csv) and (segments == set() or last_csv[-1] != max(segments)):
            segments.update(last_csv)
    # Obtain the sorted list of segment line numbers
    segment_list = sorted(list(segments))

    # Prune the segment list so that it isn't too granular
    ideal_segment_length = 100 # The ideal number of lines in a segment
    pruned_segment_list = [1]
    for i in range(1, len(segment_list)):
        if segment_list[i] - pruned_segment_list[-1] >= ideal_segment_length:
            pruned_segment_list.append(segment_list[i-1]) # Add the latest segment not exceeding the ideal length

    # Add the last segment if necessary
    if len(lines) - pruned_segment_list[-1] >= ideal_segment_length:
        assert pruned_segment_list[-1] != segment_list[-1]
        pruned_segment_list.append(segment_list[-1])

    # Return the pruned list of segments
    return pruned_segment_list
