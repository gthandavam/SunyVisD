'''
Created on Mar 21, 2013

@author: ganesathandavamponnuraj
'''

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
import xml.etree.ElementTree as etree
import numbers
#gt.wsd.hw1.graphwsd.
import pagerank.pagerank as pr
import re
from document_relatedness import *
from math import fabs as absolute
from bs4 import BeautifulSoup as bs
import nltk

filename='/home/user/Downloads/task17-test+keys/test/English/EnglishAW.test.xml'
outputfile='pagerank-output'

'''
idea: 

parsing: iterate through <s> tags. for each sentence extract the content
by regex processing. Extract the target words under <head> tag along 
with the key by xml lookup.
(single parse for the whole process)

preparation: 
data structures : all the open class words in the sentence
target words and positions
lemmatize the words
run pagerank and get the most probable sense

output:
write the data to file
'''

def get_sentence_map(tree):
 
    sent_map = {}

    for head in tree.findall("//head"):
        l=head.attrib['id'].split('.')
        if (sent_map.get(l[0]+l[1])!=None):
            sent_map[l[0]+l[1]]+=","+head.attrib['id']
        else:
            sent_map[l[0]+l[1]]=head.attrib['id']

    return sent_map       

    
def searchwl(word_map,word_list,word):
    """need to print the key to output file"""
    for key1 in word_list:
        if word_map[key1]==word:
            return key1

def pad_zeros(offset):
    offset_str=str(offset)
    ret = '00000000'+offset_str
    return ret[(len(ret)-8):]
                     
                 
def get_sentences(filename):
    tree = etree.parse(filename)
    sentences = tree.findall('.//s')
    return sentences

def get_target_words(sentence):
    tree = etree.fromstring(etree.tostring(sentence))
    target_words = tree.findall('head')
    return target_words
    
    '''
    API to remove <head> tags and give only the context words
    '''
def get_context(sentence):
    context = etree.tostring(sentence)
    context = context.lower()
    context = bs(context).text
    context = context.replace('\n', ' ') 
    return context

def get_target_words_map(sentence, context_list):
    tree = etree.fromstring(etree.tostring(sentence))
    t_words_list = [0 for i in range(len(context_list))]
    t_words = tree.findall('head')
    '''
         strong assumption that target words do not repeat in a context
         helps this implementation work
    '''
    for t_word in t_words:        
            for i in range(len(context_list)):
                if(context_list[i] == t_word.text.lower()):
                    t_words_list[i] = t_word.attrib['id']
#     print t_words_list
    return t_words_list

def remove_stop_words(context):
    #split based on one or more whitespace
    words = context.split()
    words = [word for word in words if word not in sw.words('english')]
    return words
    

    '''
    @param f : file object -> file handle to the output file
    @param context: list of words in order as present in the context
    @param tgt_words: list same length as context: contains '' or 
                        the actual id of the target word as applicable
    @param max_dist: maxDist parameter as per R.Mihalcea
    @param d_factor: damping factor for pagerank   
    '''
def process_per_sentence(f,context, tgt_words, max_dist, d_factor):
    
    print context
    word_synsets = {}
    synset_index = {}
    index = 0
        
    for i in range(len(context)):
        t_context = tuple([i,context[i]])
#         word = wn.morphy(context[i])
#         if( word == None ) :
#             word = context[i]
        word_synsets[t_context] = wn.synsets(context[i])

	
        for synset in word_synsets[t_context]:
            t_synset = tuple([i, synset])
            synset_index[t_synset] = index
#             print synset, index
            index += 1
            
    graph_matrix = [[0 for i in range(index)] for j in range(index)]
    #print indexprint [word for word in words]
       
    for i in range(len(context)):
        for j in range(len(context)):
            if i != j:
                 
                #check how far the 2 words are from each other
                if( absolute(i-j) <= max_dist ):
                     
                    for synset1 in word_synsets[ tuple([i, context[i]]) ]:
                        t_s1 = tuple([i, synset1])
                        for synset2 in word_synsets[ tuple([j, context[j]]) ]:
                            t_s2 = tuple([j, synset2])
#                             sim = synset1.wup_similarity(synset2)
			    synset_str1=synset1.name.split('.')[0]
			    synset_str2=synset2.name.split('.')[0]	
                            sim1 = ESA_similarity(synset_str1, synset_str2)
                            sim2 = ESA_similarity(synset_str2, synset_str1)
                            if isinstance(sim1, numbers.Number) == False: sim1 = 0
                            if isinstance(sim2, numbers.Number) == False: sim2 = 0
                            
                            graph_matrix[synset_index[t_s1]][synset_index[t_s2]] = sim1
                            graph_matrix[synset_index[t_s2]][synset_index[t_s1]] = sim2
 			    
    ranked_sense = pr.get_pagerank(graph_matrix, d_factor)
#     print ranked_sense
   
#process only for target_words
    for i in range(len(tgt_words)):
        if isinstance(t_words[i], numbers.Number) == False:
            word_t = tuple([i, context[i]])
#         targeword_t_id = 
            synsets = word_synsets[word_t]
            max_r = 0
            res_offset = -1
            chosen_synset = None
            for synset in synsets:
                t_synset = tuple([i, synset])
                if ranked_sense[synset_index[t_synset]] >= max_r:
                    max_r = ranked_sense[synset_index[t_synset]]
                    res_offset = synset.offset
                    chosen_synset = synset  
                    offset_str=pad_zeros(res_offset)
                    answer_line=tgt_words[i][0:3]+" "+tgt_words[i]+" eng-30-"+offset_str+"-"+chosen_synset.pos+"\n"
                    print answer_line
                    f.write(answer_line)
#     print "finished"           

        
if __name__ == '__main__':
#     filename = '/home/gt/Downloads/test/English/test.xml'
    sentences = get_sentences(filename)
    out_f = open(outputfile,'w')
#     out_f = open('/home/gt/Downloads/test/scorer2/test','w')

    punc = re.compile(r'[-.?!,":;()|/0-9]')
    for sentence in sentences:
        context = get_context(sentence)
#         
#         pos_text = nltk.word_tokenize(context)
#         pos_tags = nltk.pos_tag(pos_text)
#         print pos_tags
        context = punc.sub("", context)
        context_list = context.split()
#         context_list = remove_stop_words(context)
        print context_list
        t_words = get_target_words_map(sentence, context_list)
        print t_words
        ''' assumption: no target word is repeated in a context
            hence choosing not to maintain position of target word
            in a sentence
        '''         
        process_per_sentence(out_f, context_list, t_words, 7, 0.85)
        
    out_f.close()
        
    
