#!/usr/bin/env python

import xml.parsers.expat
import re
from nltk import PorterStemmer # or LancasterStemmer
from nltk.corpus import stopwords

IN_PATH = 'E:/Desktop/wikiprep/enwiki-2013-04-04-pages-articles.xml'
OUT_PATH = 'E:/Desktop/wikiprep/articles.txt'

TEXT_PREVIEW = 500 # use None for full text
ARTICLE_PREVIEW = 1000 # use None for all articles

BUFFER_SIZE = 16384

MIN_WORDS = 200
TITLE_WEIGHT = 4

class State(object):
	
	def __init__(self):
		self.cur_elem = None
		self.in_page = False
		self.page_id = None
		self.page_title = None
		self.page_namespace = None
		self.page_redirect = False
		self.text_pieces = []
		self.text = None
		self.num_pages = 0
		self.elements = ('text', 'title', 'ns', 'id')

state = State()

title_filters = [
	r'^List of .+', # Lists
	r'.+ \(disambiguation\)$', # disambiguation pages
	r'^(January|February|March|April|May|June|July|August|September|October|November|December) \d+$', # Months
	r'^\d+ in .+$', # Years
	r'^\d+$' # Years and numbers
]
title_filter_rx = re.compile('|'.join(title_filters), re.DOTALL | re.IGNORECASE)

def valid_concept():
	global state
	if state.page_namespace != 0: # Main namespace only
		return False
	if state.page_redirect:
		return False
	if title_filter_rx.match(state.page_title):
		return False
	if '{{disambiguation}}' in state.text: # Disambiguation templates (complete?)
		return False
	if '{{disambiguation|' in state.text:
		return False
	if '{{db-' in state.text: # Deletion templates (incomplete)
		return False
	if '{{di-' in state.text:
		return False
	if '{{dv-' in state.text:
		return False
	if '{{nn-' in state.text:
		return False
	if '{{Proposed deletion endorsed}}' in state.text:
		return False
	return True

comment_rx = re.compile(r'<!--.*?-->', re.DOTALL)
template_rx = re.compile(r'\{\{[^\{]+?}}', re.DOTALL)
math_rx = re.compile(r'<math>.*?</math>', re.DOTALL)
html_rx = re.compile(r'</?[A-Za-z]+.*?>', re.DOTALL)
link_include_rx = re.compile(r'\[\[(?:File|Image):[^\[\]]+\|(.+?)\]\]', re.DOTALL)
link_wiki_rx = re.compile(r'\[\[([^\|]+?)\]\]', re.DOTALL)
link_bar_rx = re.compile(r'\[\[[^\]]+?\|(.+?)\]\]', re.DOTALL)
link_url_rx = re.compile(r'\[[^\]\s]+ (.+?)\]', re.DOTALL)
punc_rx = re.compile(r'[^A-Za-z0-9]+', re.DOTALL)

stemmer = PorterStemmer()
stem = lambda w: stemmer.stem(stemmer.stem(stemmer.stem(w))) # stem three times
stop_words = stopwords.words('english')

def extract_words(text):
	text = re.sub(comment_rx, ' ', text) # <!--comments-->
	text = re.sub(template_rx, ' ', text) # {{a {{b {{sub-sub-template}} c}} d}}
	text = re.sub(template_rx, ' ', text) # {{a {{sub-template}} b}}
	text = re.sub(template_rx, ' ', text) # {{template}}
	text = re.sub(math_rx, ' ', text) # <math>...</math>
	text = re.sub(html_rx, ' ', text) # <html> </tags>
	text = re.sub(link_include_rx, r'\1', text) # [[File:]] [[Image:]]
	text = re.sub(link_wiki_rx, r'\1', text) # [[article]]
	text = re.sub(link_bar_rx, r'\1', text) # [[article|text]]
	text = re.sub(link_url_rx, r'\1', text) # [http://url text]
	text = re.sub(punc_rx, ' ', text) # punctuation
	text = text.lower()
	words = [stem(w) for w in text.split()]
	words = [w for w in words if w not in stop_words] # remove stop words
	return words

def parse_page():
	global state
	if not valid_concept():
		return
	state.text = ((state.page_title + ' ')
		* TITLE_WEIGHT + state.text)
	words = extract_words(state.text)
	if len(words) < MIN_WORDS:
		return
	state.text = ' '.join(words)
	outfile.write("%d\t%s\t%d\t%d\t%s\n" % (state.page_id, state.page_title,
		len(words), len(state.text), state.text[:TEXT_PREVIEW]))
	state.num_pages += 1

def start_element(name, attrs):
	global state
	state.cur_elem = name
	if name == 'page':
		state.in_page = True
		state.page_id = None
		state.page_title = None
		state.page_namespace = None
		state.page_redirect = False
		state.text_pieces = []
		state.text = None

def end_element(name):
	global state
	state.cur_elem = None
	if not state.in_page:
		return
	state.text = u''.join(state.text_pieces)
	del state.text_pieces
	state.text_pieces = []
	if name == 'text':
		state.in_page = False
		state.text = state.text.encode('ascii', 'replace')
		parse_page()
		if ARTICLE_PREVIEW and state.num_pages > ARTICLE_PREVIEW:
			raise Exception('article limit reached: %d' %
				(ARTICLE_PREVIEW,))
	elif name == 'title':
		state.page_title = state.text.encode('utf-8', 'replace')
	elif name == 'ns':
		state.page_namespace = int(state.text)
	elif name == 'id':
		state.page_id = int(state.text)
	elif name == 'redirect':
		state.page_redirect = True
	del state.text

def char_data(data):
	global state
	if state.in_page and state.cur_elem in state.elements:
		state.text_pieces.append(data)

parser = xml.parsers.expat.ParserCreate()

parser.buffer_size = BUFFER_SIZE
parser.buffer_text = True

parser.StartElementHandler = start_element
parser.EndElementHandler = end_element
parser.CharacterDataHandler = char_data

infile = open(IN_PATH, 'r')
outfile = open(OUT_PATH, 'w')

outfile.write("id\ttitle\twords\tchars\ttext\n")
parser.ParseFile(infile)

infile.close()
outfile.close()
