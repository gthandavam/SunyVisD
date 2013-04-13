'''
Created on Apr 11, 2013

@author: gt
'''

import xml.etree.ElementTree as etree
#beautiful soup library to convert html entities to text - overkill
from bs4 import BeautifulSoup as bs
import re
from nltk.corpus import stopwords as sw
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
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
    tree = etree.parse('small_dump')
    encoding = 'UTF-8'
    pages = tree.findall('.//page')
#     word_dict = {}
    document_ids = []
    document_content = []
    for page in pages:
#         print page.attrib['id']
        title = bs(etree.tostring(page.find('title'))).text
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
    x = vect.fit_transform(document_content)     
    xarr = x.toarray()
    
    transformer = TfidfTransformer()
    
    tfidf = transformer.fit_transform(xarr)
    
    mmwrite('tf_idf_scipy', tfidf)
    print document_ids