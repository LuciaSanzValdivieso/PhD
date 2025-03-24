import argparse
from collections import Counter

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Count occurrences of numbers at the end of lines in a file.")
    parser.add_argument("--file", required=True, help="Path to the input file.")
    parser.add_argument("--output", required=True, help="Path to the output file.")
    args = parser.parse_args()

    input_file = args.file
    output_file = args.output

    try:
        # Step 1: Read the file and extract numbers from the end of each line
        numbers = []
        with open(input_file, "r") as f:
            for line in f:
                # Extract the last element after splitting by whitespace
                parts = line.strip().split()
                if not parts:
                    continue  # Skip empty lines
                
                try:
                    number = int(parts[-1])  # The last element is the number
                    numbers.append(number)
                except ValueError:
                    print(f"Skipping line with invalid number: {line.strip()}")

        # Step 2: Count the occurrences of each number
        number_counts = Counter(numbers)

        # Step 3: Write the counts to the output file
        with open(output_file, "w") as out:
            for number, count in sorted(number_counts.items()):
                out.write(f"{number}: {count}\n")

        print(f"Counts written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
