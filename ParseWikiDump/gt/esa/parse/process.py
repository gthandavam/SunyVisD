# import sqlite3 as sqlite
import xml.etree.cElementTree as etree
# from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from scipy.io import mmwrite
from parse_wiki import rem_stop_words_and_stem as rswm
from parse_wiki import rem_punctuation as rp

articles_xml = 'small_dump.xml'
# tfidf_mtx = 'E:/Desktop/wikiprep/tfidf.mtx'
#tfidf_db = 'E:/Desktop/wikiprep/tfidf.db'

# stopwords_eng = set(stopwords.words('english'))
# 
# stemmer = PorterStemmer()


def process_page(page):
	# Get relevant attributes and tag content
	page_id = page.attrib['id']
	text = page.find('text').text
	print page_id +"\n";
	f = open( "file_"+str(page_id), 'w')
	text = rswm(text)
	text = rp(text)
	text = text.lower()
	f.write(text)
	f.close()
	
def process_dump(xml):
	# Parse the XML file
	print 'Parsing...',
	parsed = iter(etree.iterparse(xml, events=('start', 'end')))
	print 'Done'
	# Process all the <page> elements
	print 'Processing pages...'
	event, root = parsed.next() # <mediawiki> root
	for (event, elem) in parsed:
		if event == 'end' and elem.tag == 'page':
			process_page(elem)
		root.clear() # Avoid accumulating empty <page> elements
	print 'Done'
# 	# Count words in each concept
# 	print 'Counting words...',
# 	count_vectorizer = CountVectorizer(
# 		charset_error = 'ignore',
# 		strip_accents = 'ascii',
# 		preprocessor = stemmer.stem,
# 		stop_words = stopwords_eng,
# 		lowercase = True
# 		###vocabulary = list_of_valid_english_words
# 	)
# 	count_vecs = count_vectorizer.fit_transform(concept_texts, y=concept_ids)
# 	print 'Done'
# 	# Calculate tf-idf scores
# 	print 'Calculating tf-idf scores...',
# 	tfidf_transformer = TfidfTransformer()
# 	tfidf_vecs = tfidf_transformer.transform(count_vecs)
# 	print 'Done'
# 	# Write data
# 	print 'Writing data...',
# 	mmwrite(mtx, tfidf_vecs)
# 	print 'Done'

if __name__ == '__main__':
	print 'XML input:', articles_xml
# 	print 'MTX output:', tfidf_mtx
	process_dump(articles_xml)
