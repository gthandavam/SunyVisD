SunyVisD
========

An attempt at making a more meaningful Visual Dictionary.


1. Extract only main text from Wikipedia article.
2. Each article is a concept (concept ID)
3. Each concept has a tf-idf vector for all the words present in the concept [Let's restrict ourselves to just context words] [may be we can use wordnet to identify the comprehensive list of context words; we can remove punctuation marks using regex]
/* Needless to say that we need to take into account the entire wiki dump to come up with tf, idf values*/
4. Now we build an inverted index for the distinct words [Word ID] that says how related one word is to a concept. 
  We need to have a threshold to remove the concepts that have very low TF-IDF values, w.r.t a word. 

Given a word we can build a network that highlights concepts most related to the word.

For simplicity let's say we are given a word as input, we display n different concepts on the web-page. [We can work on making the content visually appealing, as we progress]

----- 
TABLE words (
id INT UNIQUE, -- 4-byte signed integer key, can go up to 2 billion; there should only be millions of words at most, so this is plenty
word VARCHAR(100) UNIQUE -- or however long the longest word is
)
-- example rows: (8, "cancer"), (9, "sarcoma"), (42, "rose")

TABLE concepts (
id INT UNIQUE,
concept VARCHAR(100) UNIQUE
)
-- example rows: (19, "Cancer"), (20, "Flower"), (27, "Cell (biology)")

TABLE inverted_index (
word_id INT,
concept_id INT,
tf_idf FLOAT
)
-- example rows: (8, 19, 1.0), (8, 20, 0.01), (9, 19, 0.75), (42, 20, 0.8)

