import json, os
from jsonmerge import merge

directory = ""

# create an empty list to store the merged JSON data
merged_json = []

# iterate over the files in the directory
for filename in os.scandir(directory):
    if not filename.name.endswith('.jsonl'):
        continue
    # open the file
    with open(filename, 'r') as f:
        # load the JSON data from the file
        json_data = json.load(f)
        # merge the JSON data with the existing data
        merged_json = merge(merged_json, json_data)

# write the merged JSON data to a file
with open('output.json', 'w') as f:
    json.dump(merged_json, f)
    f.close()
