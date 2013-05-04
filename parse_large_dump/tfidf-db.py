#!/usr/bin/env python

import sqlite3
import random

DB_PATH = 'E:/Desktop/wikiprep/tfidf.db'
CONCEPTS_PATH = 'E:/Desktop/wikiprep/stemmed-articles.txt'
WORDS_PATH = 'E:/Desktop/wikiprep/words-idf.txt'
TFIDF_PATH = 'E:/Desktop/wikiprep/words-tf.txt'

conn = sqlite3.connect(DB_PATH)
conn.text_factory = str
cur = conn.cursor()

print "Generating concepts..."

cur.execute('''CREATE TABLE concepts (
	id INTEGER NOT NULL PRIMARY KEY,
	concept TEXT NOT NULL
)''')

def gen_concepts():
	infile = open(CONCEPTS_PATH, 'r')
	lines_gen = infile.xreadlines()
	header = lines_gen.next()
	concept_id = 0
	for line in lines_gen:
		title, _ = line.split("\t", 1)
		yield (concept_id, title)
		if not concept_id % 18575:
			print concept_id, '/', 1857524
		concept_id += 1
	infile.close()

cur.executemany('''INSERT INTO concepts VALUES (?, ?)''',
	gen_concepts())

print "Generating words..."

cur.execute('''CREATE TABLE words (
	id INTEGER NOT NULL PRIMARY KEY,
	word TEXT NOT NULL UNIQUE
)''')

def gen_words():
	infile = open(WORDS_PATH, 'r')
	lines_gen = infile.xreadlines()
	header = lines_gen.next()
	word_id = 0
	for line in lines_gen:
		word, _ = line.split("\t", 1)
		yield (word_id, word)
		if not word_id % 63438:
			print word_id, '/', 6343823
		word_id += 1
	infile.close()

cur.executemany('''INSERT INTO words VALUES (?, ?)''',
	gen_words())

print "Generating inverted index..."

cur.execute('''CREATE TABLE inverted_index (
	word_id INTEGER NOT NULL,
	concept_id INTEGER NOT NULL,
	tfidf FLOAT NOT NULL,
	FOREIGN KEY(word_id) REFERENCES words(id),
	FOREIGN KEY(concept_id) REFERENCES concepts(id)
)''')

def gen_tfidf():
	infile = open(TFIDF_PATH, 'r')
	lines_gen = infile.xreadlines()
	header = lines_gen.next()
	entry = 0
	for line in lines_gen:
		concept_id, word_id, count, tf, tfidf = line.split("\t", 4)
		yield (int(word_id), int(concept_id), float(tfidf))
		if not entry % 583983:
			print entry, '/', 583983030
		entry += 1
	infile.close()

cur.executemany('''INSERT INTO inverted_index VALUES (?, ?, ?)''',
	gen_tfidf())

conn.close()
