Notebook (Google Colab) containing the scripts used in Technique B (terminology-based domain-specific corpus curation, dissertation section 5.3.2)

The main script (checkparaterms.py) is used to curate a downloaded big corpus into a domain-specific corpus, using the corpus and a termlist of bilingual equivalences. It filters the corpus' parallel segments that contain any of the equivalences in the termlist and outputs such segments into a curated file that contains the filtered corpus.

The complementary/preliminary scripts are used to check there is a tab separation between the corpus' parallel segments and between the termlist's equivalences respectively.

Use of the main script: python3 checkparaterms.py corpus.txt termlist.txt output.txt Use of complementary scripts: python3 check-tab-corpus.py tab-separated-parallel-segments-corpus.txt
