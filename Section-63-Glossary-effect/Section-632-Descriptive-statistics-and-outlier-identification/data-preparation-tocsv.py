# File paths
frequency_file = "analysisA-termscount.txt"  # Spanish term, tab, count
correct_file = "welltranslated-MarianA-analysis.txt"     # Terms correctly translated
incorrect_file = "wrongtranslations-MarianA-analysis.txt" # Terms incorrectly translated
output_file = "output.csv"             # Final file with appended Correct/Incorrect

# Load correct and incorrect terms into sets
with open(correct_file, "r") as corrects:
    correct_terms = set(line.strip() for line in corrects)

with open(incorrect_file, "r") as incorrects:
    incorrect_terms = set(line.strip() for line in incorrects)

# Process the frequency file
with open(frequency_file, "r") as freq_file, open(output_file, "w") as outfile:
    outfile.write("Term\tFrequency\tTranslation accuracy\n")  # Header row
    for line in freq_file:
        parts = line.strip().split("\t")
        if len(parts) == 2:  # Ensure the line has the expected format
            term, count = parts
            if term in correct_terms:
                accuracy = "Correct"
            elif term in incorrect_terms:
                accuracy = "Incorrect"
            else:
                accuracy = "Unknown"  # In case it's not in either list
            outfile.write(f"{term}\t{count}\t{accuracy}\n")
