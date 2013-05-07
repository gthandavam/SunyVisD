#!/usr/bin/env python

import math

IN_PATH_IDF = 'E:/Desktop/wikiprep/words-idf.txt'
IN_PATH_ARTICLES = 'E:/Desktop/wikiprep/stemmed-articles.txt'
OUT_PATH = 'E:/Desktop/wikiprep/words-tf.txt'

word_idfs = {}
word_ids = {}

infile = open(IN_PATH_IDF, 'r')

lines_gen = infile.xreadlines()
header = lines_gen.next()
word_id = 0
for line in lines_gen:
	word, idf, _ = line.split("\t", 2)
	word_idfs[word] = float(idf)
	word_ids[word] = word_id
	word_id += 1

infile.close()

infile = open(IN_PATH_ARTICLES, 'r')
outfile = open(OUT_PATH, 'w', 1)

outfile.write("concept id\tword id\tcount\ttf\ttf-idf\n")
lines_gen = infile.xreadlines()
header = lines_gen.next()
concept_id = 0
for line in lines_gen:
	title, text = line.split("\t")
	counts = {}
	for word in text.split():
		if word not in counts:
			counts[word] = 0
		counts[word] += 1
	max_count = max(counts.values())
	for word in counts:
		word_id = word_ids.get(word, -1)
		count = counts.get(word, 0)
		if word_id == -1: # debug
			print "*** Word without ID: %s ***" % (word,)
			print "*** Count in doc #%d: %d ***" % (concept_id, count)
		tf = math.log1p(count)
		idf = word_idfs[word]
		tf_idf = tf * idf
		outfile.write("%d\t%d\t%d\t%s\t%s\n" % (concept_id,
			word_id, count, repr(tf), repr(tf_idf)))
	del counts
	concept_id += 1

infile.close()
outfile.close()
