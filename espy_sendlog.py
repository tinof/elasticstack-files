import os
import json
import logging

from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

# Configuration start

es_hosts = [
    "http://localhost:9200",
]

es_api_user = 'elastic'
es_api_password = 'changeme'

index_name = ''

chunk_size = 10000

errors_before_interrupt = 5

refresh_index_after_insert = False

max_insert_retries = 3

yield_ok = False  # if False will skip successful documents in the output

# Configuration end

filename = ""

logging.info('Importing data from {}'.format(filename))

es = Elasticsearch(
    es_hosts,
    basic_auth=(es_api_user, es_api_password),
    retry_on_timeout=True  # should timeout trigger a retry on different node?
)


def data_generator():
    # Open the file
    f = open(filename)

    # Initialize the progress bar
    pbar = tqdm(total=os.path.getsize(filename))

    for line in f:
        yield {**json.loads(line), **{
            "_index": index_name,
        }}

        # Update the progress bar
        pbar.update(len(line))

    # Close the progress bar
    pbar.close()


errors_count = 0

for ok, result in streaming_bulk(es, data_generator(), chunk_size=chunk_size,
                                 refresh=refresh_index_after_insert,
                                 max_retries=max_insert_retries,
                                 yield_ok=yield_ok):
    if ok is not True:
        logging.error('Failed to import data')
        logging.error(str(result))
        errors_count += 1

        if errors_count == errors_before_interrupt:
            logging.fatal('Too many import errors, exiting with error code')
            exit(1)
