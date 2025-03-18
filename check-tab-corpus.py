import codecs

corpus = "tab-separated-parallel-segments-corpus.txt"  # Replace with corpus file

with codecs.open(corpus, "r", encoding="utf-8") as file:
    for line_num, line in enumerate(file, start=1):
        if "\t" not in line:
            print(f"Error in line {line_num} of the corpus: {line.strip()}")
