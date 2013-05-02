enwiki-latest-pages-articles.xml:
40.4 GB
13,675,673 pages
Downloaded April 4, 2013 from http://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia

stem-articles.py:
Parses the Wikipedia database dump. Rejects articles that are redirects,
proposed for deletion, or are too short. Stems the words in the remaining
articles.

stemmed-articles.txt:
7.52 GB
1,857,524 articles

idf-words.py:
Calculates the IDF score for each word in the stemmed articles.

TODO: calculate TF, and TF-IDF, scores.
