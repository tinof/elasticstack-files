import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm

es_hosts = [
    "http://localhost:9200",
]

es_api_user = 'elastic'
es_api_password = 'changeme'

# The path to the folder containing the files to be imported
folder_path = ""

# The name of the Elasticsearch index to which the data will be imported
index_name = ""

# The Elasticsearch client
es = Elasticsearch(es_hosts, basic_auth=(es_api_user, es_api_password))

# Create an empty list to store the paths of the files in the folder
file_paths = []

# Use the os.listdir() function to get a list of the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file has the ".jsonl" extension
    if filename.endswith(".jsonl"):
        # Construct the full path to the file and append it to the list of file paths
        file_paths.append(os.path.join(folder_path, filename))


# Define a function that processes a single file
def process_file(file_path):
    # Open the file for reading
    with open(file_path, "r") as f:
        # Read the lines in the file
        for line in f:
            yield {**json.loads(line), **{
                "_index": index_name,
            }}


# Use the ThreadPoolExecutor to process the files in parallel
with ThreadPoolExecutor() as executor:
    # Create a progress bar
    with tqdm(total=len(file_paths)) as pbar:
        # Submit the tasks to the executor
        futures = [executor.submit(process_file, file_path) for file_path in file_paths]

        # Iterate over the completed tasks
        for future in as_completed(futures):
            # Get the data from the task
            data = future.result()

            # Use the Elasticsearch bulk API to insert the data into Elasticsearch
            helpers.bulk(es, data)

            # Update the progress bar
            pbar.update(1)

    pbar.close()

