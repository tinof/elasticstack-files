import json
import os
from tqdm import tqdm

directory = '/Users/tinoftu/Downloads/dataa/kartta.kokkola.fi/rikastettu'

# Check all jsonl files in a directory for errors
def check_jsonl_files(directory):
    # Iterate over each jsonl file in the directory
    for filename in tqdm(os.listdir(directory), desc="Checking files"):
        if not filename.endswith('.jsonl'):
            continue
        # Open the file
        with open(os.path.join(directory, filename), 'r') as f:
            # Iterate over each line in the file
            for i, line in enumerate(f):
                try:
                    # Parse the line as JSON
                    json.loads(line)
                except json.decoder.JSONDecodeError as e:
                    # Print the error
                    print(f'Error on line {i+1} of {filename}: {e}')




# Merge all jsonl files in a directory into one file
def merge_jsonl_files(directory):
    # Create a list to store the lines
    lines = []

    # Iterate over each file in the directory
    for filename in tqdm(os.listdir(directory), desc="Merging files"):
        # Open the file
        with open(os.path.join(directory, filename), 'r') as f:
            # Iterate over each line in the file
            for line in f:
                # Add the line to the list of lines
                lines.append(line)

    # Open the output file
    with open(os.path.join(directory, 'merged.jsonl'), 'w') as f:
        # Write the lines to the output file
        f.write(''.join(lines))

#merge_jsonl_files(directory)
check_jsonl_files(directory)