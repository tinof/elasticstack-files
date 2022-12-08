##UnicodeDecodeError
import os
import json

# Set the directory containing the JSONL files
directory = '/Users/tinoftu/Downloads/dataa/kartta.kokkola.fi/rikastettu'

# Loop through all files in the directory and Log an error message if the UnicodeDecodeError is raised
for filename in os.listdir(directory):
    try:
        with open(os.path.join(directory, filename), 'r') as f:
            for line in f:
                json.loads(line)
    except UnicodeDecodeError as e:
        print(f'Error on file {filename}: {e}')


