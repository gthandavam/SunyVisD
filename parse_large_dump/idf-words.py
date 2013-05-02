#!/usr/bin/env python

import math

IN_PATH = 'E:/Desktop/wikiprep/stemmed-articles.txt'
OUT_PATH = 'E:/Desktop/wikiprep/words-idf.txt'

total_count = {}
doc_count = {}

infile = open(IN_PATH, 'r')
outfile = open(OUT_PATH, 'w', 1)

for line in infile.xreadlines():
	id, title, nwords, nchars, text = line.split("\t")
	if id == "id": # header
		continue
	words = text.split()
	seen_words = set()
	for word in words:
		if word not in total_count:
			total_count[word] = 0
			doc_count[word] = 0
		total_count[word] += 1
		if word not in seen_words:
			doc_count[word] += 1
			seen_words.add(word)

num_docs = 1857524 # from stemmed-articles.txt
log_num_docs = math.log(num_docs)

outfile.write("word\tidf\tnum docs with word\ttotal uses of word\n")
for (word, dc) in reversed(sorted(doc_count.items(), key=lambda x: x[1])):
	idf = log_num_docs - math.log(dc)
	outfile.write("%s\t%s\t%d\t%d\n" % (word, repr(idf), dc, total_count[word]))

infile.close()
outfile.close()
