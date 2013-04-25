SunyVisD
========

An attempt at making a more meaningful Visual Dictionary.

1. Extract the main text from Wikipedia article. Remove HTML/Wiki markup and stop words.
2. Each article is a concept -- a sequence of words with an ID number.
3. Calculate a tf-idf vector for each concept, with the tf-idf scores for each context word in the article.
    * We could restrict context words to a certain set, like those with WordNet synsets, or everything thats in nltk.corpus.words but not nltk.corpus.stopwords
    * Needless to say that we need to take into account the entire wiki dump to get tf-idf values
4. Now we build an inverted index for the distinct words [Word ID] that says how related one word is to a concept. 
    * We need to have a threshold to remove the concepts that have very low tf-idf values w.r.t. the word. 

Given a word we can build a network that highlights concepts most related to the word.

For simplicity let's say we are given a word as input, we display n different concepts on the web-page. [We can work on making the content visually appealing, as we progress]

Database Schema
===============

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

Librarires Used
===============

Beautiful Soup - For removing the HTML entities from the text.
 * This might be overkill; assuming Wikipedia doesn't have lots of badly-formed HTML, we could use regex to remove `<[^>]+>`
sklearn 0.10 -> TfidfTransformer, CountVectorizer
