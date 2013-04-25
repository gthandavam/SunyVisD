'''
Created on Apr 11, 2013
computes cosine similarity
@author: Okhazamov
'''

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

size_of_vocab=700
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
        cosine_distance = lambda a, b : round(np.inner(a, b)/(LA.norm(a)*LA.norm(b)), 3)
        stemmer=PorterStemmer()
        word1=stemmer.stem("article")
        word2=stemmer.stem("text")
        
        
        
        A = np.ones((size_of_vocab,1), np.float32 )
        B = np.ones((size_of_vocab,1), np.float32 )
        Read_IDF_Array("/home/user/workspace/VisuWords/perl_parse_wiki/inverted_tf/"+word1+"_inverted_idx",A)
        Read_IDF_Array("/home/user/workspace/VisuWords/perl_parse_wiki/inverted_tf/"+word2+"_inverted_idx",B)
        Aflat = np.hstack( A )
        Bflat = np.hstack( B )
        dist = distance.cosine(Aflat,Bflat)

        
        print "Cosine distance"
        print dist                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    
     