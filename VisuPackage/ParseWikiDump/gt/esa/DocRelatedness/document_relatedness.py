'''
Created on Apr 11, 2013

@author: Okhazamov
'''

import xml.etree.ElementTree as etree
#beautiful soup library to convert html entities to text - overkill
from bs4 import BeautifulSoup as bs
import re
from nltk.corpus import stopwords as sw
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.spatial.distance import cosine
from scipy.io import mmwrite

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

if __name__ == '__main__':
    #try:
        tree = etree.parse('small_dump')
    
        related_text=open("text",'r')
    
        text = related_text.read()
        text = rem_stop_words_and_stem(rem_punctuation(text.lower()))
        input_document_ids = []
        input_document_content = [] 
    
    
        encoding = 'UTF-8'
    
#     word_dict = {}
    
#         print page.attrib['id']
        title = text[0]
        #title 
#         print title
       #print text
        
        input_document_ids.append(1)
        input_document_content.append(text)
#         words = text.split()
#         for word in words:
#             if( word in word_dict ):
#                 word_dict[word] += 1
#             else: 
#                 word_dict[word] = 1
#         print "******************************************"
    
    #tf idf of input document
        encoding = 'UTF-8'
        pages = tree.findall('.//page')
#     word_dict = {}
        document_ids = []
        document_content = [] 
    #tf_idf of wikipedia articles
        for page in pages:
#         print page.attrib['id']
            title = bs(etree.tostring(page.find('title'))).text
            #title 
#         print title
            text = bs(etree.tostring(page.find('text'))).text
            text = rem_stop_words_and_stem(rem_punctuation(text.lower()))
#         print text
            document_ids.append(page.attrib['id'])
            document_content.append(text)
#         words = text.split()
#         for word in words:
#             if( word in word_dict ):
#                 word_dict[word] += 1
#             else: 
#                 word_dict[word] = 1
#         print "******************************************"
    
        vect = CountVectorizer()     
        vect_input = CountVectorizer(min_df=0.5)
    
        x = vect.fit_transform(document_content)     
        #print x
        y = vect_input.fit_transform(input_document_content)
        xarr = x.toarray()    
        yarr = y.toarray()
        
            
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(xarr)
    
    #use centroid classifierw
    #compute cosine similarity between two documents
        distance=0
        #output top-10 concepts
        #for (int i=0; i<size(xarr,1); ++i)
        distance=cosine(xarr[0],yarr)
            
        print "Cosine distance"
        print distance                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    
            #top-10
        mmwrite('tf_idf_scipy', tfidf)
        print document_ids
    #except Exception, e:
        #logger.critical( "Failed to create file \"%s\" : %s" % ( filename, e ) 
                         