#!/usr/bin/env python

import xml.parsers.expat
import re
import textwrap

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

template_rx = re.compile(r'\{\{.+?}}', re.DOTALL)
math_rx = re.compile(r'<math>.*?</math>', re.DOTALL)
html_rx = re.compile(r'</?[A-Za-z]+.*?>', re.DOTALL)
comment_rx = re.compile(r'<!--.*?-->', re.DOTALL)
link_file_rx = re.compile(r'\[\[File:.+?\]\]', re.DOTALL)
link_wiki_rx = re.compile(r'\[\[([^\|]+?)\]\]', re.DOTALL)
link_bar_rx = re.compile(r'\[\[[^\]]+?\|(.+?)\]\]', re.DOTALL)
link_url_rx = re.compile(r'\[[^\]\s]+ (.+?)\]', re.DOTALL)
punc_rx = re.compile(r'\W+', re.DOTALL)

def strip_markup(s):
	s = re.sub(template_rx, ' ', s) # remove templates
	s = re.sub(math_rx, ' ', s) # remove <math></math>
	s = re.sub(html_rx, ' ', s) # remove HTML tags
	s = re.sub(comment_rx, ' ', s) # remove HTML comments
	s = re.sub(link_file_rx, ' ', s) # remove [[File:includes]
	s = re.sub(link_wiki_rx, r'\1', s) # unlinkify [[links]]
	s = re.sub(link_bar_rx, r'\1', s) # unlinkify [[wiki|links]]
	s = re.sub(link_url_rx, r'\1', s) # unlinkify [http:// links]
	s = re.sub(punc_rx, ' ', s) # remove punctuation
	return s

def parse_page():
	if state.page_namespace != 0: # Main namespace only
		return
	if state.page_redirect:
		return
	if title_filter_rx.match(state.page_title):
		return
	state.text = strip_markup(state.text)
	print "%d\t%s\t%d" % (state.page_id, state.page_title, len(state.text))

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

parser.buffer_size = 16384
parser.buffer_text = True

parser.StartElementHandler = start_element
parser.EndElementHandler = end_element
parser.CharacterDataHandler = char_data

path = r'E:/Desktop/wikiprep/enwiki-latest-pages-articles.xml'
file = open(path, 'r')
depth = 0
parser.ParseFile(file)
file.close()
