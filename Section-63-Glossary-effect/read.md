### TO STUDY TERMS IN A PARALLEL CORPUS  6.3
Files needed: sample to translate, translated sample by system 1, translated sample by system 2, 
glossary, training dataset(s) (A, B1 and B2 in the dissertation) + scripts

#### IN MONOLINGUAL SAMPLE, WITH BILINGUAL TERMLIST #### 6.3.1

# To keep only the source expressions from a bilingual termlist that has the format "source expression, tab, target expression":
	cut -f1 bil-termlist.txt > mono-termlist.txt

# To identify the glossary Spanish (source) terms in a monolingual Spanish sample. Two outputs: terms and segments where they are, both with counts.
	python3 monoterm-check-2output.py monol-corpus.txt mono-termlist.txt output-mono-terms.txt output-mono-segments.txt 
# To sum the counts in output-terms.txt and know types/tokens:
		python3 sum-numbers-mono.py --file output-mono-terms.txt --output sum-output-mono-terms.txt

# To strip the numbers from the term output file for the next step:
	cut -f1 output-mono-terms.txt > termsinsample-monol.txt

#To identify the equivalences prescribed by the glossary/bilingual termlist for those terms present in the monolingual source corpus, 
# i.e., the expected correct equivalences to look for in the translations:
		python3 matchmonotermstobilglossary.py --file1 bil-termlist.txt --file2 termsinsample-monol.txt --output termsinsample-bil.txt



#### IN BILINGUAL SAMPLE/TRANSLATIONS and PARALLEL TRAINING DATASETS, WITH BILINGUAL TERMLIST OF TERMS IN SAMPLE (from previous step) #### 
# REPEAT WITH EACH SYSTEMS' TRANSLATIONS and WITH DIFFERENT DATASETS, TO GET COUNTS (6.3.1 with translations, 6.3.2 with training datasets)
# To see what terms from the bilingual glossary are in the translations/training datasets, and you get again two outputs, 
# one counting pairs of equivalences, and one printing all segments with a count of the terms occuring in each segment.
	python3 paraterm-check-2outputs.py translation.txt/datasetAnotB.txt termsinsample-bil.txt outputsampleintrainingAnotB-terms.txt outputsampleintrainingAnotB-segments.txt
### The first output file xyz-terms.txt has "SL expression, tab, TL expression, tab, occurrences" format, to be used for ANALYSIS explained below

# To count source terms and not pairs of equivalences 
# (en nariz as a single type, and not en nariz=on the nose and en nariz=in the nose as two types), edit collapsing-repeated-slterms.py
		python3 collapsing-repeated-slterms.py 
  [will join lines with matching Spanish and different target, and sum counts of both]

# In second output file, segments: first count how many 0 matches, then deduct from total line count (total segments) (wc -l):
			grep "0 matches" outputsampleintrainingAnotB-segments.txt | wc -l
			wc -l outputsampleintrainingAnotB-segments.txt

# In first output file (-terms): to get a sum of all the occurrences of all terms (tokens):
	python3 sum-numbers.py --file outputsampleintrainingAnotB-terms.txt --output sum-outputsampleintrainingAnotB.txt
# Count lines to know how many different terms (types):
	wc -l outputsampleintrainingAnotB-terms.txt
# Count how many terms occur once, twice, thrice, etc. in the format "occurrences: numbers of terms occuring that many times": (NOT USED IN DISSERTATION)
	python3 counter-occurrences.py --file outputsampleintrainingAnotB-terms.txt --output countsAnotB.txt

# To take out the number in the "expression, tab, expression, ta, count" -term.txt files, do:
	cut -f1,2 outputsampleinGoogle-terms.txt > outputsampleinGoogle-terms-nonum.txt


#### TO PREPARE THESE FILES FOR ANALYSIS #### repeat for each system's translations/training dataset (6.3.2)

# To compare terms (or lines) that are the same or different in two files (first smaller file, then bigger file)
# Use the command lines below to get well-translated (identical lines) and wrongly translated (different) lines (equivalences) in the systems' translations
# by extracting the identical equivalences from the -term.txt outputs (well-tranlsated)
# and by taking out those identical (well translated) equivalences from the bilingual termlist of equivalences in sample, remaining the wrongly translated

## We do this identical/different comparison to be able to append "Correct" or "Incorrect" to each of the equivalences the glossary contemplated for the source terms in the Spanish sample,
# done in the next step using data-preparation-tocsv.py (see below) which gives us a csv file for analysis.	
	grep -vFxf outputsampleinGoogle-terms-nonum.txt termsinsample-bil.txt > wrongtranslations-Google.txt
	grep -Fxf outputsampleinGoogle-terms-nonum.txt termsinsample-bil.txt > welltranslated-Google.txt
	
#Careful, the lines must match in format (trailing spaces...), so do this first:
# To see hidden characters:
	cat -A output-terms-Google-nonum.txt
 # To homogeneize, first bigger file, than smaller file:
	sed -i 's/[ \t]*$//' outputsampleinGoogle-terms-nonum.txt termlist-original.txt
	sed -i 's/\r$//' outputsampleinGoogle-terms-nonum.txt termlist-original.txt
# To further check if ther format matches:
	file outputsampleinGoogle-terms-nonum.txt termlist-original.txt
	#if they dont match: dos2unix outputsampleinGoogle-terms-nonum.txt termlist-original.txt


# To turn paratermcheck.py -term.txt files (equiv. freq. in training datasets) from "expression, tab, expression, tab, count" into
# "expression [SL and TL as a single one w/o tabs], tab, count" NECESSARY for data preparation analysis
	awk -F"\t" '{print $1,$2 "\t" $3}' outputsampleintrainingB1-terms.txt > analysisB1-termscount.txt

# To replace the tab between the SL and TL expressions in the well-translated and wrong-translations files to allow for comparison with the termscount file that contains the frequency of the equivalences in the training data:
	awk -F"\t" '{print $1,$2}' wrongtranslations-MarianA.txt > wrongtranslations-MarianA-analysis.txt


#### TO ANALYZE ### (6.3.2.1, 6.3.2.2 and 6.3.2.3)

# To give data csv format for analysis, nano data-preparation-tocsv.py
	frequency_file = "analysisA-termscount.txt"  # Equivalence, tab, count (occurrences in training dataset, from last step) 
	correct_file = "welltranslated-MarianA-analysis.txt"     # Terms correctly translated (from previous step above)
	incorrect_file = "wrongtranslations-MarianA-analysis.txt" # Terms incorrectly translated
	output_file = "analysis-dataMarianA-DatasetA.csv"             # Final file with Term. equivalece, Freq, and Correct/Incorrect
 
 # The output csv file should look like: 
	# Term	Frequency	Translation Accuracy
	# agradable plush	34	Incorrect
	# amargor medio medium bitterness	21	Correct
	# amplio mouth-filling	5	Incorrect

# Then replace "Correct" and "Incorrect" with "0" and "1":
	python3 mappingnumericvalues.py # Edit it to replace with name of file to run it on

# The output file is good to perform descriptive statistics (6.3.2.1 with outliers, and 6.3.2.2, without outliers):
	python3 data-analysis-destats.py # Edit to replace with name of file to run it on

# Then, use command lines to add a "System" column at the end, which should include the same of each system (MarianA or Weights): 
	sed -E '1s/$/\tSystem/; 2,$s/$/\tMarianA/' file-with-no-system-column.csv > file-with-system-column.csv
# so the file looks like:
		# Term	Frequency	Translation accuracy	System
		# agradable plush	23	0	MarianA
		# amargor medio medium bitterness	17	0	MarianA
		# AOVE EVOO	1025	1	Weights
		# aceite de oliva olive oil	70814	1	Weights
		# aroma nose	649	0	Weights

# These processes (descriptive statistics) can be repeated after identifying and eliminating outliers (6.3.2.2):

# Plot to visualize data distribution to check whether the data is skewed
			python3 visualization-datadistribution.py  # Edit input filename

# IQR analysis to identify outliers to eliminate
			python3 quartileid.py # Edit input filename and define output name for the file free of outliers according to the IQR


## Last, to perform a logistic regression to predict the impact of frequency on accuracy, use the Colab notebook logistic-regression-model-study (6.3.2.3). These scripts take as input the csv file contains both systems' data.
