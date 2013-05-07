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
import sqlite3
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
DB_PATH="/media/Windows7_OS/linguistics/tfidf-d80-t1.75.db"

        
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
def Read_IDF_ArrayDB(cur, word,A):
	query='SELECT concept_id,tfidf FROM inverted_index as II, words as W WHERE II.word_id=W.id and W.word="'+word+'"'
	cur.execute(query)
	data_rows_A=cur.fetchall()
	for row in data_rows_A:
		print row[0],row[1]
		A[row[0]]=row[1]




#	word_file=open("idf_file","r")
#	word1=word_file.readline()
#	while word1:
#  		word1=stemmer.stem(word1).rstrip('1234567890\n\t\r ')
#
 #       	A = np.ones((size_of_vocab,1), np.float32)
#		print "word1",word1	
#		filename1="/home/user/workspace/VisuWords/perl_parse_wiki/inverted_tf/"+word1+"_inverted_idx"	
#	
#		#exists=os.path.exists(filename1)
#		#print filename1, exists
#		if os.path.exists(filename1):		
#			Read_IDF_Array(filename1,A)
#			Aflat = np.hstack(A)
#			word2=word_file.readline()
 #       		while word2:
#				print "word2",word2
 #                       	word2=stemmer.stem(word2).rstrip('1234567890\n\t\r ')
  #                      	filename2="/home/user/workspace/VisuWords/perl_parse_wiki/inverted_tf/"+word2+"_inverted_idx"
#				B = np.ones((size_of_vocab,1), np.float32)
#				if os.path.exists(filename2):                        
#					Read_IDF_Array(filename2,B)
#				Bflat = np.hstack(B)
 #       	        	dist = distance.cosine(Aflat,Bflat)
#				print "Cosine distance between ",word1,word2,"  ",dist,"\n"
#				word2=word_file.readline()
#		position+=len(word1)+1        	
#		word_file.seek(position,0)
#		word1=word_file.readline()
 
	

def ESA_similarity(word1,word2):
     #try:	
	#select word from word id
	 	 
	query=""
	dist=0
	#define cosine distance
	cosine_distance = lambda a, b : round(np.inner(a, b)/(LA.norm(a)*LA.norm(b)))
	#nlogn file reads will be performed, position - s position pointer
	position=0  
	
	connect=sqlite3.connect(DB_PATH)
        cur=connect.cursor()

	#get the number of concepts 
	cur.execute('SELECT COUNT(*) FROM concepts')
	size_of_vocab=int(cur.fetchone()[0])
	print size_of_vocab
	
	A = np.ones((size_of_vocab,1), np.float32)
	B = np.ones((size_of_vocab,1), np.float32)
	Read_IDF_ArrayDB(cur,word1, A) 
	Read_IDF_ArrayDB(cur,word2, B)
	Aflat = np.hstack(A)
	Bflat = np.hstack(B)
	#for x in range(A.size):
        #        if A[x]>1: print x,A[x]

	dist=cosine_distance(Aflat,Bflat)
	return dist
    # except sqlite3.Error, e:
    
   #	 print "Error %s:" % e.args[0]
    #	 sys.exit(1)
    
     #finally:
    
    	#if connect:
        #	connect.close()


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    
     
