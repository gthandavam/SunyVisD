This script is used to parse the 41GB Wikipedia dump from April 2013.
WikiPrep has not been run on the dump, so it has to remove HTML/Wiki markup
and figure out categories itself.

It uses the streaming expat parser to read enwiki-latest-pages-articles.xml.
So far it identifies articles that fit the following criteria:
 * Not a redirect
 * Not a disambiguation page
We'll also need to check later that the articles meet a minimum length, and
that they aren't in certain stop categories.

After verifying that an article is good and should be counted as a concept,
the script will extract its text, stem it, and create the tf-idf inverted
index.
