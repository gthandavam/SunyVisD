'''
Created on Apr 11, 2013

@author: gt
'''

import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup as bs
import re
from nltk.corpus import stopwords as sw
 #beautiful soup library to convert html entities to text - overkill
 
def rem_stop_words(text):
    #split based on one or more whitespace
    words = text.split()
    text = ''
    for word in words:
        if(word not in sw.words('english')):
            text = text + word + ' '
            
    return text
 
def rem_punctuation(text):
    punc = re.compile(r'[#-.?!,":;()|/0-9]')  
    punc.sub('', text) 
    return text 

if __name__ == '__main__':
    tree = etree.parse('small_dump')
    encoding = 'UTF-8'
    pages = tree.findall('.//page')
    
    for page in pages:
        print page.attrib['id']
        title = bs(etree.tostring(page.find('title'))).text
        print title
        text = bs(etree.tostring(page.find('text'))).text
        text = rem_stop_words(rem_punctuation(text))
        print text
        print "******************************************"
    
    
    
    
      
        