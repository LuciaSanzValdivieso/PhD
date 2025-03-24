# TO IDENTIFY THE GLOSSARY EQUIVALENCES FOR THE MONOLINGUAL TERMS IN THE SOURCE SAMPLE
# AND THEREFORE IDENTIFY THE PAIRS OF EQUIVALENT TERMS THAT ARE CORRECT
# TO BE ABLE TO CHECK WHETHER THE TRANSLATIONS DO COMPLY WITH THOSE EQUIVALENCES
import argparse
from collections import defaultdict

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Match expressions and write bilingual equivalents.")
    parser.add_argument("--file1", required=True, help="Path to the bilingual glossary (File 1).")
    parser.add_argument("--file2", required=True, help="Path to the monolingual expressions file (File 2).")
    parser.add_argument("--output", required=True, help="Path to the output file.")
    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    output_file = args.output

    try:
        # Step 1: Read File 1 and build a dictionary mapping expressions in language A to their equivalents in language B
        glossary = defaultdict(list)
        with open(file1, "r") as f1:
            for line in f1:
                parts = line.strip().split("\t")
                if len(parts) != 2:
                    print(f"Skipping malformed line in File 1: {line}")
                    continue
                lang_a, lang_b = parts
                glossary[lang_a].append(lang_b)

        # Step 2: Read File 2 and find matches from the glossary
        with open(file2, "r") as f2:
            expressions = [line.strip() for line in f2 if line.strip()]

        # Step 3: Write the results to the output file
        with open(output_file, "w") as out:
            for expr in expressions:
                equivalents = glossary.get(expr, [])
                if equivalents:
                    for equivalent in equivalents:
                        out.write(f"{expr}\t{equivalent}\n")
                else:
                    print(f"No match found for expression: {expr}")

        print(f"Output written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
