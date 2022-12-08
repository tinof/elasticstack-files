import os
import gzip
import json
from tqdm import tqdm

# Set the path to the folder containing the .gz files
folder_path = '/Users/tinoftu/Downloads/dataa/kartta.kokkola.fi/rikastettu'

# Initialize the progress bar
pbar = tqdm(total=len(os.listdir(folder_path)))

# Create an empty list to store the .jsonl files
jsonl_files = []

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a .gz file
    if filename.endswith('.gz'):
        # Open the .gz file and extract the contents
        with gzip.open(os.path.join(folder_path, filename), 'rb') as f:
            # Write the contents to a new .jsonl file
            jsonl_filename = filename[:-3] + '.jsonl'
            with open(os.path.join(folder_path, jsonl_filename), 'wb') as g:
                g.write(f.read())

            # Add the .jsonl file to the list
            jsonl_files.append(jsonl_filename)

    # Update the progress bar
    pbar.update(1)
    pbar.set_description("Extracting .gz files")

# Close the progress bar
pbar.close()

# Initialize a new progress bar
pbar = tqdm(total=len(jsonl_files))

# Create an empty list to store the JSON objects
json_objects = []

# Iterate over the .jsonl files
for filename in jsonl_files:
    # Open the .jsonl file and read the contents
    with open(os.path.join(folder_path, filename), 'r') as f:
        # Iterate over each line in the file
        for line in f:
            # Parse the line as JSON and add it to the list of JSON objects
            json_objects.append(json.loads(line))

    pbar.update(1)
    pbar.set_description("Reading .jsonl files")

pbar.close()

pbar = tqdm(total=len(json_objects))

# Write the JSON objects to a single .jsonl file
with open(os.path.join(folder_path, 'combined.jsonl'), 'w') as f:
    for obj in json_objects:
        f.write(json.dumps(obj) + '\n')
        pbar.update(1)
        pbar.set_description("Writing combined.jsonl file")

pbar.close()
