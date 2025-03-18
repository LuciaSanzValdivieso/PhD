import codecs
import sys
import re

# Use: python3 checkparaterms.py corpus.txt termlist.txt output.txt
# Complementary files: check-tab-corpus.py and check-tab-termlist.py to check correct formatting

corpus = sys.argv[1]
termlist = sys.argv[2]
nomsortida = sys.argv[3]

termsfile = codecs.open(termlist, "r", encoding="utf-8")
termstuples = {}

for termpair in termsfile:
    termpair = termpair.strip()
    termstuples[termpair] = 0

termsfile.close()

entrada = codecs.open(corpus, "r", encoding="utf-8")

sortida = codecs.open(nomsortida, "w", encoding="utf-8")

cont = 0
for linia in entrada:
    cont += 1
    linia = linia.rstrip()
    camps = linia.split("\t")
    if len(camps) < 2:
        print(f"Error: Line {cont} does not match the expected format: {linia}")
        continue
    
    segeng = camps[0]
    segspa = camps[1]
    
    for tp in termstuples:
        camps = tp.split("\t")
        eng = camps[0]
        spas = camps[1].split(":")
        regexp = re.compile(r'\b{0}\b'.format(re.escape(eng)), re.IGNORECASE)
        found = False
        if re.search(regexp, segeng):
            for spa in spas:
                regexp2 = re.compile(r'\b{0}\b'.format(re.escape(spa)), re.IGNORECASE)
                if re.search(regexp2, segspa):
                    found = True
                    break
        if found:
            sortida.write("{0}\t{1}\n".format(segeng, segspa))

sortida.close()
