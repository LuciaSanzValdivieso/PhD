### TO IDENTIFY TERMS FROM MONOLINGUAL TERMLIST IN MONOLINGUAL CORPUS
# LONGEST MATCH ("sweet aroma of" over "aroma of")
import codecs
import sys
import re

corpus = sys.argv[1]          # Path to the corpus file
termlist = sys.argv[2]        # Path to the term list file
nomsortida = sys.argv[3]      # Output file for term frequencies
segment_output = sys.argv[4]  # Output file for terms per segment

# Step 1: Load and sort terms by length (largest first, for longest matches first)
termsfile = codecs.open(termlist, "r", encoding="utf-8")
term_counts = {}

for term in termsfile:
    term = term.strip()
    if term:  # Ensure non-empty term
        term_counts[term] = 0

termsfile.close()

# Sort terms by length in descending order (to match longer terms first)
sorted_terms = sorted(term_counts.keys(), key=len, reverse=True)

# Step 2: Process the corpus file
entrada = codecs.open(corpus, "r", encoding="utf-8")

segment_matches = {}  # Dictionary to store matched terms per segment
segment_number = 0

for line in entrada:
    segment_number += 1
    line = line.rstrip()
    
    matched_spans = []  # Track positions of matched spans to avoid overlap
    segment_matches[segment_number] = []  # Initialize entry for the current segment

    for term in sorted_terms:
        # Compile regex for the term with re.IGNORECASE for case-insensitive matching
        regexp = re.compile(r'\b{0}\b'.format(re.escape(term)), re.IGNORECASE)
        term_match = re.search(regexp, line)

        if term_match:
            term_span = term_match.span()  # Get the span (start and end positions) of the term

            # Check for overlap with previously matched spans
            if any(start <= term_span[0] < end or start < term_span[1] <= end for start, end in matched_spans):
                continue  # Skip this term if it overlaps with a larger match already found

            # Update the global count for the term
            term_counts[term] += 1
            matched_spans.append(term_span)  # Add the span to matched spans

            # Append matched term for segment-based output
            segment_matches[segment_number].append(term)

    # If no terms were matched in this segment, add "No matches" to indicate that
    if not segment_matches[segment_number]:
        segment_matches[segment_number] = ["No matches"]

entrada.close()

# Step 3: Write term frequency output to the first output file
with codecs.open(nomsortida, "w", encoding="utf-8") as output_file:
    for term, count in term_counts.items():
        if count > 0:
            output_file.write(f"{term}\t{count}\n")

# Step 4: Write segment-based output to the second output file with match count
with codecs.open(segment_output, "w", encoding="utf-8") as segment_output_file:
    for segment, terms in segment_matches.items():
        # Join terms found in this segment with a semicolon
        terms_str = "; ".join(terms)
        match_count = len(terms) if "No matches" not in terms else 0
        segment_output_file.write(f"{segment} [segment {segment}] {terms_str} [{match_count} match{'es' if match_count != 1 else ''}]\n")