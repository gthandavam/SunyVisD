#!/usr/bin/env python

import xml.parsers.expat
import re
from nltk import PorterStemmer # or LancasterStemmer

IN_PATH = 'E:/Desktop/wikiprep/enwiki-2013-04-04-pages-articles.xml'
OUT_PATH = 'E:/Desktop/wikiprep/articles.txt'

TEXT_PREVIEW = 500 # use None for full text
ARTICLE_PREVIEW = 1000 # use None for all articles

BUFFER_SIZE = 16384

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

comment_rx = re.compile(r'<!--.*?-->', re.DOTALL)
template_rx = re.compile(r'\{\{[^\{]+?}}', re.DOTALL)
math_rx = re.compile(r'<math>.*?</math>', re.DOTALL)
html_rx = re.compile(r'</?[A-Za-z]+.*?>', re.DOTALL)
link_include_rx = re.compile(r'\[\[(?:File|Image):[^\[\]]+\|(.+?)\]\]', re.DOTALL)
link_wiki_rx = re.compile(r'\[\[([^\|]+?)\]\]', re.DOTALL)
link_bar_rx = re.compile(r'\[\[[^\]]+?\|(.+?)\]\]', re.DOTALL)
link_url_rx = re.compile(r'\[[^\]\s]+ (.+?)\]', re.DOTALL)
punc_rx = re.compile(r'[^A-Za-z]+', re.DOTALL)

def strip_markup(s):
	s = re.sub(comment_rx, ' ', s) # <!--comments-->
	s = re.sub(template_rx, ' ', s) # {{a {{b {{sub-sub-template}} c}} d}}
	s = re.sub(template_rx, ' ', s) # {{a {{sub-template}} b}}
	s = re.sub(template_rx, ' ', s) # {{template}}
	s = re.sub(math_rx, ' ', s) # <math>...</math>
	s = re.sub(html_rx, ' ', s) # <html> </tags>
	s = re.sub(link_include_rx, r'\1', s) # [[File:]] [[Image:]]
	s = re.sub(link_wiki_rx, r'\1', s) # [[article]]
	s = re.sub(link_bar_rx, r'\1', s) # [[article|text]]
	s = re.sub(link_url_rx, r'\1', s) # [http://url text]
	s = re.sub(punc_rx, ' ', s) # punctuation
	s = s.lower()
	return s

stemmer = PorterStemmer()

def stem(s):
	return [stemmer.stem(w) for w in s.split()]

title_filters = [
	r'^List of .+', # Lists
	r'.+ \(disambiguation\)$', # disambiguation pages
	r'^(January|February|March|April|May|June|July|August|September|October|November|December) \d+$', # Months
	r'^\d+ in .+$', # Years
	r'^\d+$' # Years and numbers
]
title_filter_rx = re.compile('|'.join(title_filters), re.DOTALL | re.IGNORECASE)

def parse_page():
	global state
	if state.page_namespace != 0: # Main namespace only
		return
	if state.page_redirect:
		return
	if title_filter_rx.match(state.page_title):
		return
	state.text = strip_markup(state.text)
	state.text = stem(state.text)
	text = ' '.join(state.text)
	outfile.write("%d\t%s\t%d\t%d\t%s\n" % (state.page_id, state.page_title,
		len(state.text), len(text), text[:TEXT_PREVIEW]))
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
