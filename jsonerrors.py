##UnicodeDecodeError
import os
import json


directory = ''

for filename in os.listdir(directory):
    try:
        with open(os.path.join(directory, filename), 'r') as f:
            for line in f:
                json.loads(line)
    except UnicodeDecodeError as e:
        print(f'Error on file {filename}: {e}')


