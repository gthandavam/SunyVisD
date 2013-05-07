Workflow:

1. Download `[enwiki-latest-pages-articles.xml](http://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia)`
   (40.4 GB, 13,675,673 pages), an XML dump of Wikipedia's database from April 4, 2013.

2. Run `stem-articles.py` to: parse the Wikipedia dump; reject articles that
   are redirects, proposed for deletion, or are too short; and stem the words
   in the remaining articles. The output is `stemmed-articles.txt` (7.52 GB,
   1,857,524 articles).

3. Run `idf-words.py` to: calculate the IDF score for each word in the stemmed
   articles. The output is `words-idf.txt` (197 MB, 6,343,823 words).

4. Run `tf-words.py` to: calculate the TF and TF-IDF scores for the (concept,
   word) pairs, using the concepts/articles from `stemmed-articles.txt` and the
   words from `words-idf.txt`. The output is `words-tf.txt` (29.7 GB,
   583,983,030 (concept, word) pairs).

5. Run `tfidf-db.py` to: create an SQLite database with the tables `concepts`,
   `words`, and `inverted_index`. The inverted index rejects entries with a
   TF-IDF score below a certain threshold, or with words not found in the
   stemmed SCOWL dictionary.
