#!/usr/bin/env python

import xml.parsers.expat
import re

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

def parse_page():
	if state.page_namespace != u'0': # Main namespace only
		return
	if state.page_redirect:
		return
	if title_filter_rx.match(state.page_title):
		return
	print state.page_id, '=', state.page_title

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
	state.text = ''.join(state.text_pieces)
	del state.text_pieces
	state.text_pieces = []
	if name == 'page':
		state.in_page = False
		parse_page()
	elif name == 'title':
		state.page_title = state.text
	elif name == 'ns':
		state.page_namespace = state.text
	elif name == 'id':
		state.page_id = state.text
	elif name == 'redirect':
		state.page_redirect = True
	del state.text

def char_data(data):
	global state
	if state.in_page and state.cur_elem in state.elements:
		text = data.encode('ascii', 'ignore')
		state.text_pieces.append(text)

parser = xml.parsers.expat.ParserCreate()

parser.buffer_size = 8192
parser.buffer_text = True

parser.StartElementHandler = start_element
parser.EndElementHandler = end_element
parser.CharacterDataHandler = char_data

path = r'E:/Desktop/wikiprep/enwiki-latest-pages-articles.xml'
file = open(path, 'r')
depth = 0
parser.ParseFile(file)
file.close()
