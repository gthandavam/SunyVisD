#!/usr/bin/env python

import math

IN_PATH_IDF = 'E:/Desktop/wikiprep/words-idf.txt'
IN_PATH_ARTICLES = 'E:/Desktop/wikiprep/stemmed-articles.txt'
OUT_PATH = 'E:/Desktop/wikiprep/words-tf.txt'

word_idfs = {}
word_ids = {}

infile = open(IN_PATH_IDF, 'r')

word_id = 0
for line in infile.xreadlines():
	word, idf, _ = line.split("\t", 2)
	if word == "word" and idf == "idf": # skip header
		continue
	word_idfs[word] = float(idf)
	word_ids[word] = word_id
	word_id += 1

infile.close()

infile = open(IN_PATH_ARTICLES, 'r')
outfile = open(OUT_PATH, 'w', 1)

outfile.write("concept id\tword id\tcount\ttf\ttf-idf\n")
concept_id = 0
for line in infile.xreadlines():
	title, text = line.split("\t")
	if title == "title" and text == "text": # skip header
		continue
	counts = {}
	words = text.split()
	del text
	for word in words:
		if word not in counts:
			counts[word] = 0
		counts[word] += 1
	del words
	max_count = max(counts.values())
	for word in counts:
		word_id = word_ids[word]
		count = counts[word]
		tf = math.log1p(count)
		idf = word_idfs[word]
		tf_idf = tf * idf
		outfile.write("%d\t%d\t%d\t%s\t%s\n" % (concept_id,
			word_id, count, repr(tf), repr(tf_idf)))
	del counts
	concept_id += 1

infile.close()
outfile.close()
