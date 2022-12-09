import os
import ujson
import tqdm

# Merge all jsonl files in a directory into one file
def merge_jsonl_files(directory):
    # Create a list to store the lines
    lines = []

    # Define a function to convert JSON data to a Python object
    def json_object_hook(obj):
        return {k.lower(): v for k, v in obj.items()}

    for filename in os.scandir(directory):
        if not filename.name.endswith('.jsonl'):
            continue
        # Open the file
        with open(filename, 'r') as f:
            # Iterate over each line in the file
            for line in f:
                # Parse the line as JSON using the json_object_hook function
                json_obj = ujson.loads(line, object_hook=json_object_hook)
                # Add the line to the list of lines
                lines.append(ujson.dumps(json_obj))

    # Open the output file
    with open(os.path.join(directory, 'merged.jsonl'), 'w') as f:
        # Initialize the progress bar
        pbar = tqdm.tqdm(total=len(lines), desc="Writing lines to file")

        # Write the lines to the output file
        for line in lines:
            f.write(line)
            f.write('\n')
            # Update the progress bar
            pbar.update(1)

        # Close the progress bar
        pbar.close()

        # Close the output file
        f.close()


merge_jsonl_files('/Users/tinoftu/Downloads/dataa/kartta.kokkola.fi/rikastettu')