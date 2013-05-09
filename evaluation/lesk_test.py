import nltk
import re
from sets import Set
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import xml.etree.ElementTree as etree
from document_relatedness import *
path_string='./small_EnglishAW.test.xml'  

#root=getroot('/home/user/Downloads/task17-test+keys/test/English/EnglishAW.test.xml')
#root.xpath('/corpus/text/*/text()')

'''
    @param - filename @type string -> filename pathpath_string that contains the sem-eval test data [EnglishAW.text.xml file]
    @return - returns a dictionary: key -> id of the head tag in the sem-eval task 17 document @type string
                                    value-> word to be disambiguated @type string
'''

#takes a tree and a word key and returns a sentence which contains that word

def get_sentence(tree,key):
   sentence=""
   text_id=""
   for text in tree.findall("//s"):
     #print text_id=
     for head in text.iter():
     #print head
      if head.tag=="head": 
       if head.attrib['id']==key:
              for s in text.itertext():
                  sentence+=s
   sentence=sentence.replace("\n", " ")
   return sentence              
        
    
    
    

def get_wsd_input_data(tree):
    
        
# xml file comes without a namespace; so looking up for all the head tags within the document,
#without specifying the namespace
#Ref: http://getpython3.com/diveintopython3/xml.html#xml-parse
    
    heads = tree.findall("//head")    
    
    ret_dictionary = {}
    
    for head in heads:
#        print head.attrib['id']," " + head.text
        ret_dictionary[head.attrib['id']] = head.text
    return ret_dictionary    
        
 
         
    
        
    
    

def get_context_words(sentence):          #extracts content words and converts them to the base form
    if sentence!="":
      tokens=wordpunct_tokenize(sentence)
    #text = nltk.Text(tokens)
      words = [wn.morphy(w.lower()) if wn.morphy(w.lower())!=None else w.lower() for w in tokens] 
      return tokens



def computeoverlap(sig1,sig2):            #need to know how many words have in common
    w=""
    k=0
    overlap=set.intersection(sig1,sig2)
    for w in overlap:
      if len(w)>3: k+=1
    return k




def split_syn_dots(word):
    w=""
    l=[]
    for ch in word:
      if ch!='.':
        w=w+ch
      else:
        l.append(w)
        w=""
    l.append(w)
    return l 

def lesk_ESA_similarity(filename):
 	
	print "Lesk ESA"
	f = open(filename,'w')
	tree = etree.parse(path_string)
	dictionary = get_wsd_input_data(tree);
	print "Computing Lesk  Similarity  \n"
	for key in sorted(dictionary.iterkeys()):
   		word=wn.morphy(dictionary[key].lower())
	sentence=get_sentence(tree,key)
  	context_original=set([]) 

  	for w in get_context_words(sentence):
         if w.isdigit()==False:
            context_original.add(w) 
            if wn.lemmas(w)!=[]:
           	def_sentence=wn.lemmas(w)[0].synset.definition
           	for mmm in get_context_words(def_sentence):
             		context_original.add(mmm)
         
  
  	best_sense=wn.lemmas(word)[0].synset  #best sense    #most frequent sense is a default one
 	max_overlap=1000000
  	for lemma in wn.lemmas(word):
    		context_int=set([])
    		for example in lemma.synset.examples:        
        		for w in get_context_words(example):
            			context_int.add(w)
    		for w in get_context_words(lemma.synset.definition):   
        		context_int.add(w)
    		overlap=ESA_sentence_similarity(context_original,context_int)
    		if overlap<max_overlap: 
        		max_overlap=overlap
        		best_sense=lemma.synset
  	l=split_syn_dots(key)
   
  	answer_line=l[0]+" "+key+" eng-30-"+str(best_sense.offset)+"-"+best_sense.pos+"\n"
  	f.write(answer_line)
	print "Finished"

def lesk_baseline(filename):
 	
	print "Lesk Baseline"
	f = open(filename,'w')
	tree = etree.parse(path_string)
	dictionary = get_wsd_input_data(tree);
	print "Computing Lesk  Similarity  \n"
	for key in sorted(dictionary.iterkeys()):
   		word=wn.morphy(dictionary[key].lower())
	sentence=get_sentence(tree,key)
  	context_original=set([]) 

  	for w in get_context_words(sentence):
         if w.isdigit()==False:
            context_original.add(w) 
            if wn.lemmas(w)!=[]:
           	def_sentence=wn.lemmas(w)[0].synset.definition
           	for mmm in get_context_words(def_sentence):
             		context_original.add(mmm)
         
  
  	best_sense=wn.lemmas(word)[0].synset  #best sense    #most frequent sense is a default one
 	max_overlap=0
  	for lemma in wn.lemmas(word):
    		context_int=set([])
    		for example in lemma.synset.examples:        
        		for w in get_context_words(example):
            			context_int.add(w)
    		for w in get_context_words(lemma.synset.definition):   
        		context_int.add(w)
    		overlap=computeoverlap(context_original,context_int)
    		if overlap>max_overlap: 
        		max_overlap=overlap
        		best_sense=lemma.synset
  	l=split_syn_dots(key)
   
  	answer_line=l[0]+" "+key+" eng-30-"+str(best_sense.offset)+"-"+best_sense.pos+"\n"
  	f.write(answer_line)
	print "Finished"

lesk()
