#This script counts the terms from a bilingual glossary in a parallel corpus 
#and outputs two files: one contains the terms and their total number of occurrences in the corpus 
#and the other contains the total corpus segments followed by the matches it contains. 
#Case insensitive and largest span that is matched from termlist is counted.
import codecs
import sys
import re

corpus = sys.argv[1]
termlist = sys.argv[2]
nomsortida = sys.argv[3]
segment_output = sys.argv[4]  # New argument for the segment-based output file

# Step 1: Load and sort terms by length (largest first)
termsfile = codecs.open(termlist, "r", encoding="utf-8")
termstuples = {}

for termpair in termsfile:
    termpair = termpair.strip()
    # Only process lines with a tab separating two terms
    if "\t" in termpair:
        termstuples[termpair] = 0

termsfile.close()

# Sort terms by length of the English term in descending order
sorted_terms = sorted(termstuples.keys(), key=lambda x: -len(x.split("\t")[0]))

# Step 2: Process the corpus file
entrada = codecs.open(corpus, "r", encoding="utf-8")

cont = 0
segment_matches = {}  # Dictionary to store matched terms per segment

for linia in entrada:
    cont += 1
    linia = linia.rstrip()
    linia = linia.rstrip(" ")  # Remove any trailing whitespace
    camps = linia.split("\t")

    # Only proceed if there are at least two tab-separated fields
    if len(camps) > 1:
        segeng = camps[0]
        segspa = camps[1]
        
        matched_spans = []  # Track positions of matched spans to avoid overlap
        segment_matches[cont] = []  # Initialize entry for the current segment

        for tp in sorted_terms:
            camps = tp.split("\t")
            eng = camps[0]
            spas = camps[1].split(":")

            # Compile regex for the English term with re.IGNORECASE for case insensitivity
            regexp = re.compile(r'\b{0}\b'.format(re.escape(eng)), re.IGNORECASE)
            eng_match = re.search(regexp, segeng)

            if eng_match:
                eng_span = eng_match.span()  # Get the span (start and end positions) of the English term

                # Check for overlap with any previously matched spans
                if any(start <= eng_span[0] < end or start < eng_span[1] <= end for start, end in matched_spans):
                    continue  # Skip this term if it overlaps with a larger match already found

                for spa in spas:
                    # Compile regex for the Spanish term with re.IGNORECASE for case insensitivity
                    regexp2 = re.compile(r'\b{0}\b'.format(re.escape(spa)), re.IGNORECASE)
                    spa_match = re.search(regexp2, segspa)
                    if spa_match:
                        termstuples[tp] += 1
                        matched_spans.append(eng_span)  # Add the span to matched spans

                        # Append matched term for segment-based output
                        segment_matches[cont].append(f"{tp}")

                        break  # Stop further checks for this term

        # If no terms were matched in this segment, add "No matches" to the segment
        if not segment_matches[cont]:
            segment_matches[cont] = ["No matches"]

entrada.close()

# Step 3: Write term frequency output to the first output file
sortida = codecs.open(nomsortida, "w", encoding="utf-8")
for tp in termstuples:
    if termstuples[tp] > 0:
        cadena = tp + "\t" + str(termstuples[tp])
        print(cadena)
        sortida.write(cadena + "\n")
sortida.close()

# Step 4: Write segment-based output to the second output file with match count
segment_output_file = codecs.open(segment_output, "w", encoding="utf-8")
for segment, terms in segment_matches.items():
    # Join terms found in this segment with a semicolon, formatted as "English term -> Spanish term"
    terms_str = "; ".join([f"{term}" for term in terms])
    match_count = len(terms) if "No matches" not in terms else 0
    segment_output_file.write(f"{segment} [segment {segment}] {terms_str} [{match_count} match{'es' if match_count != 1 else ''}]\n")
segment_output_file.close()