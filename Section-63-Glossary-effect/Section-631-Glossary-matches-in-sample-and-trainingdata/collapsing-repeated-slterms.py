# consolidate_frequencies.py

# Define the input and output file names
input_file = 'outputsampleinB1-terms.txt'  # Replace with your file's name
output_file = 'norepe-outputsampleinB1-terms.txt'

# Dictionary to store the sum of frequencies for each Spanish expression
frequency_map = {}

# Open the input file and process each line
with open(input_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        parts = line.strip().split('\t')
        if len(parts) != 3:
            continue  # Skip malformed lines
        spanish_expr, _, freq = parts
        freq = int(freq)
        if spanish_expr in frequency_map:
            frequency_map[spanish_expr] += freq
        else:
            frequency_map[spanish_expr] = freq

# Write the consolidated results to the output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    for spanish_expr, total_freq in frequency_map.items():
        outfile.write(f"{spanish_expr}\t{total_freq}\n")

print(f"Consolidation complete. Results written to {output_file}.")
