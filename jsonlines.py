filename = ''

line_count = 0

# Open the .jsonl file in read-only mode
with open(filename, 'r') as f:
    # Iterate over each line in the file
    for line in f:
        # Increment the line counter
        line_count += 1

        # Save the current line as the last line
        last_line = line

print(f"The file has {line_count} lines.")
print(f"The last line is: {last_line}")
