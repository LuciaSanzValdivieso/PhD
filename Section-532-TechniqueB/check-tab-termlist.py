import codecs

termlist = "tab-separated-equivalents-termlist.txt"  # Replace with term list file

with codecs.open(termlist, "r", encoding="utf-8") as file:
    for line_num, line in enumerate(file, start=1):
        if "\t" not in line:
            print(f"Error in line {line_num} of the term list: {line.strip()}")
