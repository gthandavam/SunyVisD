#!/usr/bin/env python

import math

IN_PATH = 'E:/Desktop/wikiprep/stemmed-articles.txt'
OUT_PATH = 'E:/Desktop/wikiprep/words-idf.txt'

total_count = {}
doc_count = {}

infile = open(IN_PATH, 'r')
outfile = open(OUT_PATH, 'w', 1)

lines_gen = infile.xreadlines()
header = lines_gen.next()
for line in lines_gen:
	title, text = line.split("\t")
	seen_words = set()
	for word in text.split():
		if word not in total_count:
			total_count[word] = 0
			doc_count[word] = 0
		total_count[word] += 1
		if word not in seen_words:
			doc_count[word] += 1
			seen_words.add(word)
	del seen_words

num_docs = 1857524 # from stemmed-articles.txt
log_num_docs = math.log(num_docs)

outfile.write("word\tidf\tnum docs with word\ttotal uses of word\n")
for word in doc_count:
	count = doc_count[word]
	idf = log_num_docs - math.log(count)
	outfile.write("%s\t%s\t%d\t%d\n" % (word, repr(idf), count, total_count[word]))

infile.close()
outfile.close()
