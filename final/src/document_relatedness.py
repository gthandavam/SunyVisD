'''
Created on Apr 11, 2013
computes cosine similarity
@author: Okhazamov
'''
#!/usr/bin/python
import xml.etree.ElementTree as etree
from itertools import cycle
from math import sqrt
#beautiful soup library to convert html entities to text - overkill
from bs4 import BeautifulSoup as bs
import re
from time import time
from itertools import izip
from nltk.corpus import stopwords as sw
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.io import mmwrite
import sqlite3
from collections import defaultdict
import unicodedata
import StringIO
import numpy as np
from scipy.spatial import distance
from  curses.ascii import * 
import numpy.linalg as LA
import os.path
from itertools import imap
from operator import mul
#number of words
#which is half the number of files in inverted_tf file
#cosine_distance = lambda a, b : round(np.inner(a, b)/(1+LA.norm(a)*LA.norm(b)))


def cosine_distance(a, b):
    if len(a) != len(b):
    	raise ValueError, "a and b must be same length" #Steve
    numerator = 0
    denoma = 1
    denomb = 1
    for i in range(len(a)):       #Mike's optimizations:
    	ai = a[i]             #only calculate once
    	bi = b[i]
    	numerator += ai*bi    #faster than exponent (barely)
    	denoma += ai*ai       #strip abs() since it's squaring
    	denomb += bi*bi
    result = numerator / (sqrt(denoma)*sqrt(denomb))
    return result

class Document_Relatedness(object):
	def __init__(self):
		
		self.size_of_vocab=1857524
		self.DB_PATH="/host/linguistics/tfidf-d80-t2.5-indexed-tfidf-desc.db" 
		self.connect=sqlite3.connect(self.DB_PATH)
		self.cur=self.connect.cursor()
        #	self.cur.execute('SELECT COUNT(*) FROM concepts')
	#	self.size_of_vocab=int(self.cur.fetchone()[0]) 

	def rem_stop_words_and_stem(text):
    		#split based on one or more whitespace
    		p_stemmer = PorterStemmer()    		
		words = text.split()
    		text = ''
    		for word in words:
        		if(word not in sw.words('english')):
            			text = text + p_stemmer.stem(word) + ' '
            
    		return text
 
	def rem_punctuation(text):
    		punc = re.compile(r'[#-.?!,":;()|/0-9]')  
    		text = punc.sub('', text) 
    		return text 


#from IDF from file

	def Read_IDF_Array(filename, A):
    		concept_string=""
    		value=""
    		rows=""
    		with open(filename,"r") as f1:
			   while True:  
            		 	rows=f1.readline()
            			if rows=="": break
            			str_list=rows.split("\t")
            			if len(str_list)<=1: 
                			str_list=rows.split()
            			list_cycle=cycle(str_list)
            
            			concept_string=list_cycle.next()
            			for s in concept_string.split("_"):
                    			if s.isdigit():
                        			concept_id=int(s)  
            			value=float(list_cycle.next())
            			A[concept_id] = value
    		f1.close()


#read IDF from DB
	def Read_IDF_ArrayDB(self,word,A):
	  word=re.sub('[!~\' @#$]', '', word)
	  if word!='':
		t0=time()
		print "querying DB"
		query="SELECT  concept_id, tfidf from inverted_index ii join words w on ii.word_id = w.id WHERE w.word = '" +word+ "'and ii.tfidf>3;" 
		print query		
		self.cur.execute(query)
		t01=time()
		print "querying DB finished: ",t01-t0
		t0=time()
		print "fetching DATA"
		rows=self.cur.fetchall()
		t01=time()
		print "fetching DATA finished: ", t01-t0
		t1 = time()
		for row in rows:
		#	print word, row[0],row[1]
			if row[1]>=0:
				A[row[0]]=row[1]
                t2 = time()
		print "Assigning words to array  ", t2-t1        	



	def Read_Sentence_IDF(self, sentence,Acc_array):
		
		for word in sentence: 	  
			A = np.zeros((self.size_of_vocab,1), np.float32)	
			self.Read_IDF_ArrayDB(word, A)
			Acc_array+=A 
	
 
	def ESA_sentence_similarity(self,sentence1,sentence2):
     #try:	
	#select word from word id
		query=""
		dist=0
		position=0
		Accum_A=np.zeros((self.size_of_vocab,1), np.float32)
		Accum_B=np.zeros((self.size_of_vocab,1), np.float32)
		self.Read_Sentence_IDF(sentence1,Accum_A) 
		self.Read_Sentence_IDF(sentence2,Accum_B) 
		Aflat = np.hstack(Accum_A)
		Bflat = np.hstack(Accum_B)
		dist=cosine_distance(Aflat,Bflat)
		return dist	

	def ESA_word_similarity(self, word1,word2):
     	     try:	
	#select word from word id
	 	 
		query=""
		dist=0 
		position=0  
	
	
 
		A = np.zeros((self.size_of_vocab,1), object)
		B = np.zeros((self.size_of_vocab,1), object)
		print "word1"
		self.Read_IDF_ArrayDB(word1, A) 
		print "word2"
		self.Read_IDF_ArrayDB(word2, B)
		Aflat = np.hstack(A)
		Bflat = np.hstack(B)
		print "computing cosine similarity"
		t1=time()
		dist=cosine_distance(Aflat,Bflat)
		t2=time()
		print "cosine: ",t2-t1
		return dist
    # except sqlite3.Error, e:
    
   #	 print "Error %s:" % e.args[0]
    #	 sys.exit(1)
    
     	     finally:
    
    	       if self.connect:
        	 self.connect.close()


if __name__ == "__main__":
	print "******************"
	document_relatedness = Document_Relatedness()
	#print  document_relatedness.ESA_word_similarity('mirror','ipad')
	print  document_relatedness.ESA_sentence_similarity('I love being American'.split(),'I hate Russians'.split())
	 

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    
     
