'''
Created on Apr 11, 2013
computes cosine similarity
@author: Okhazamov
'''
#!/usr/bin/python
import xml.etree.ElementTree as etree
from itertools import cycle
#beautiful soup library to convert html entities to text - overkill
from bs4 import BeautifulSoup as bs
import re
from nltk.corpus import stopwords as sw
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.io import mmwrite
import re
from collections import defaultdict
import unicodedata
import StringIO
import numpy as np
from scipy.spatial import distance
from  curses.ascii import * 
import numpy.linalg as LA
import os.path
#number of words
#which is half the number of files in inverted_tf file
size_of_vocab=4000
def cosine_similarity(u,v):
    dist=distance.cosine(u, v)
    return dist

        
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

if __name__ == '__main__':
    try:	
	#define cosine distance
	cosine_distance = lambda a, b : round(np.inner(a, b)/(LA.norm(a)*LA.norm(b)))
	#nlogn file reads will be performed, position - is position pointer
	position=0
        stemmer=PorterStemmer()
	word_file=open("idf_file","r")
	word1=word_file.readline()
	while word1:
  		word1=stemmer.stem(word1).rstrip('1234567890\n\t\r ')

        	A = np.ones((size_of_vocab,1), np.float32)
		print "word1",word1	
		filename1="/home/user/workspace/VisuWords/perl_parse_wiki/inverted_tf/"+word1+"_inverted_idx"	
	
		#exists=os.path.exists(filename1)
		#print filename1, exists
		if os.path.exists(filename1):		
			Read_IDF_Array(filename1,A)
			Aflat = np.hstack(A)
			word2=word_file.readline()
        		while word2:
				print "word2",word2
                        	word2=stemmer.stem(word2).rstrip('1234567890\n\t\r ')
                        	filename2="/home/user/workspace/VisuWords/perl_parse_wiki/inverted_tf/"+word2+"_inverted_idx"
				B = np.ones((size_of_vocab,1), np.float32)
				if os.path.exists(filename2):                        
					Read_IDF_Array(filename2,B)
				Bflat = np.hstack(B)
        	        	dist = distance.cosine(Aflat,Bflat)
				print "Cosine distance between ",word1,word2,"  ",dist,"\n"
				word2=word_file.readline()
		position+=len(word1)+1        	
		word_file.seek(position,0)
		word1=word_file.readline()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    except  IOError:
	print "File error, possibly unknown word"
     
