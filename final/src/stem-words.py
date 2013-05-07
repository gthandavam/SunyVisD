#!/usr/bin/env python

from nltk import PorterStemmer # or LancasterStemmer
from nltk.corpus import stopwords

IN_PATH = 'E:/Desktop/wikiprep/scowl-words-95.txt'
OUT_PATH = 'E:/Desktop/wikiprep/scowl-words-95-stemmed.txt'

infile = open(IN_PATH, 'r')
outfile = open(OUT_PATH, 'w')

stemmer = PorterStemmer()
stem = lambda w: stemmer.stem(stemmer.stem(stemmer.stem(w))) # stem three times
stop_words = map(stem, stopwords.words('english'))

for line in infile.xreadlines():
	word = stem(line.strip())
	if word in stop_words:
		continue
	outfile.write(word + "\n")

infile.close()
outfile.close()
