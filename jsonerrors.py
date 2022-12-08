from tqdm import tqdm
import os
import json

filename = ""

# Open the JSONL file in read-write mode
with open(filename, 'r+') as f:
    # Initialize the progress bar
    pbar = tqdm(total=os.path.getsize(filename))

    # Create a list to store the fixed lines
    fixed_lines = []

    # Iterate over each line in the file
    for i, line in enumerate(f):
        try:
            # Parse the line as JSON
            json.loads(line)

            # If the line is valid JSON, add it to the list of fixed lines
            fixed_lines.append(line)
        except json.decoder.JSONDecodeError as e:
            # Check if the error is due to an unterminated string
            if 'Unterminated string starting at' in str(e):
                # Find the index of the starting quotation mark
                start_index = int(str(e).split(':')[-1])

                # Find the index of the ending quotation mark
                end_index = line[start_index:].index('"') + start_index

                # Insert the missing quotation mark
                fixed_line = line[:end_index] + '"' + line[end_index:]
                try:
                    json.loads(fixed_line)
                    fixed_lines.append(fixed_line)
                except json.decoder.JSONDecodeError as e:
                    print(f'Error on line {i+1}: {e}')
            else:
                print(f'Error on line {i+1}: {e}')

        # Update the progress bar
        pbar.update(len(line))

    # Rewind the file pointer to the beginning of the file
    f.seek(0)

    # Overwrite the file with the fixed lines
    f.write(''.join(fixed_lines))

    # Truncate the file to remove any extra data
    f.truncate()

    # Close the progress bar
    pbar.close()
