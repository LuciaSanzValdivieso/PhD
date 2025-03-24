import argparse

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Sum numbers from lines of a file.")
    parser.add_argument("--file", required=True, help="Path to the input file.")
    parser.add_argument("--output", required=True, help="Path to the output file.")
    args = parser.parse_args()

    input_file = args.file
    output_file = args.output

    try:
        total_sum = 0

        # Read the input file and calculate the sum
        with open(input_file, "r") as f:
            for line in f:
                # Strip the line of trailing whitespace and split it by tabs
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    print(f"Skipping malformed line: {line}")
                    continue
                
                try:
                    # Extract the number and add it to the total sum
                    number = float(parts[1])
                    total_sum += number
                except ValueError:
                    print(f"Skipping line with invalid number: {line}")
        
        # Write the total sum to the output file
        with open(output_file, "w") as f:
            f.write(f"{total_sum}\n")
        
        print(f"Sum written to {output_file}: {total_sum}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
