#!/usr/bin/env python

import sqlite3
import random

DB_PATH = 'E:/Desktop/wikiprep/tfidf-80.db'
CONCEPTS_PATH = 'E:/Desktop/wikiprep/stemmed-articles.txt'
WORDS_PATH = 'E:/Desktop/wikiprep/words-idf.txt'
TFIDF_PATH = 'E:/Desktop/wikiprep/words-tf.txt'
DICT_PATH = 'E:/Desktop/wikiprep/scowl-80-stemmed.txt'

NUM_ENTRIES = 583983030

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
		concept_id += 1
	infile.close()

cur.executemany('''INSERT INTO concepts VALUES (?, ?)''',
	gen_concepts())

print "Generating dictionary..."

dictionary = set()

def make_dict():
	global dictionary
	infile = open(DICT_PATH, 'r')
	dictionary.update(infile.read().split())

make_dict()

print "Generating words..."

cur.execute('''CREATE TABLE words (
	id INTEGER NOT NULL PRIMARY KEY,
	word TEXT NOT NULL UNIQUE
)''')

words = []

def gen_words():
	global words
	infile = open(WORDS_PATH, 'r')
	lines_gen = infile.xreadlines()
	header = lines_gen.next()
	word_id = 0
	for line in lines_gen:
		word, _ = line.split("\t", 1)
		words.append(word)
		if word in dictionary:
			yield (word_id, word)
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

def gen_500k_tfidf():
	global entry, words
	for _ in xrange(500000):
		line = lines_gen.next()
		concept_id, word_id, count, tf, tfidf = line.split("\t", 4)
		concept_id = int(concept_id)
		word_id = int(word_id)
		tfidf = float(tfidf)
		if words[word_id] in dictionary:
			yield (int(word_id), int(concept_id), float(tfidf))
		entry += 1
		if entry >= NUM_ENTRIES:
			break

infile = open(TFIDF_PATH, 'r')
lines_gen = infile.xreadlines()
header = lines_gen.next()
entry = 0
while entry < NUM_ENTRIES:
	cur.executemany('''INSERT INTO inverted_index VALUES (?, ?, ?)''',
		gen_500k_tfidf())
	count = cur.execute('SELECT COUNT(*) FROM inverted_index').fetchone()[0]
	print count, '/', NUM_ENTRIES
infile.close()

conn.commit()

count = cur.execute('SELECT COUNT(*) FROM inverted_index').fetchone()[0]
print 'Total:', count, '/', NUM_ENTRIES

conn.close()
