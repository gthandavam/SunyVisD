'''
Created on Mar 13, 2013

@author: ganesathandavamponnuraj
'''

from nltk.corpus import wordnet as wn
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
import xml.etree.ElementTree as etree
import numbers
import gt.wsd.hw1.graphwsd.pagerank.pagerank as pr
#import gt.wsd.hw1.graphwsd.lesk_test.get_sentence_dicts as get_sentence_map
from nltk.corpus import wordnet_ic as wic
from math import fabs as absolute
ENGLISH_xml_path="/home/user/Downloads/task17-test+keys/test/English/EnglishAW.test_en1.xml"
'''
idea: 

context is sentence:
get different senses for the words in the context from wordnet 
[extension: filter the set of feasible senses parsed on POS Tag - pre-processing]
 and find co-occurrence similarity between labels of different words -> this gives us
 the edge weights

build a graph for each of the sentences that we are trying to disambiguate

choose a graph structure

and then perform pagerank on the graph (one run per instance) to yield 
the most probable sense for the word

'''
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

def get_sentence_map(tree):
    text_id=""
    dict = {}
   
    for head in tree.findall("//head"):
             #   if head.attrib['id']!=None:
                    l=split_syn_dots(head.attrib['id'])
                    if (dict.get(l[0]+l[1])!=None):
                            #if (head.attrib['id'])
                            dict[l[0]+l[1]]+=","+head.attrib['id']
                    else:
                            dict[l[0]+l[1]]=head.attrib['id']
                  #sentence+=s
                  
   #sentence=sentence.replace("\n", " ")
    return dict       
 
def get_word_map(filename):
    tree = etree.parse(filename)
        
# xml file comes without a namespace; so looking up for all the head tags within the document,
#without specifying the namespace
#Ref: http://getpython3.com/diveintopython3/xml.html#xml-parse
    heads = tree.findall("//head")    
    
    ret_dictionary = {}
    
    for head in heads:
#        print head.attrib['id']," " + head.text
        ret_dictionary[head.attrib['id']] = head.text
        
    return ret_dictionary    


def wn_pos_dist():
    """Count the Synsets in each WordNet POS category."""
    # One-dimensional count dict with 0 as the default value:
    cats = defaultdict(int)
    # The counting loop:
    for synset in wn.all_synsets():
        cats[synset.pos] += 1
    # Print the results to the screen:
   #  for tag, count in cats.items():
   #     print tag, count
    # Total number (sum of the above):
   # print 'Total', sum(cats.values())
    
def searchwl(word_map,word_list,word):
    """need to print the key to output file"""
    for key1 in word_list:
       if word_map[key1]==word:
           return key1

def pad_zeros(offset):
    offset_str=str(offset)
    for i in range(8-len(offset_str)):
        offset_str='0'+offset_str        
    return offset_str
    
def process_per_sentence(f,words_list, word_map, max_dist, d_factor):
     
    word_synsets = {}
    synset_index = {}
    index = 0
    word_position = {}
    words = []
    
    for word_id in words_list:
        words.append(word_map[word_id])
        word_position[word_map[word_id]] = int(word_id.split(".")[2][1:])
        
    for word in words:
        word_synsets[word] = wn.synsets(word)
        for synset in word_synsets[word]:
            synset_index[synset] = index
            #print synset, index
            index += 1
#        length += len(word_synsets[word])
    graph_matrix = [[0 for i in range(index)] for j in range(index)]
    #print indexprint [word for word in words]
    
    for word1 in words:
        for word2 in words:
            if word1 != word2:
                
                #check how far the 2 words are from each other
                if( absolute(word_position[word1] - word_position[word2]) <= max_dist ):
                    
                    for synset1 in word_synsets[word1]:
                        for synset2 in word_synsets[word2]:
                            sim = synset1.path_similarity(synset2)
                            if isinstance(sim, numbers.Number) == False: sim = 0
                            graph_matrix[synset_index[synset1]][synset_index[synset2]] = sim
                            graph_matrix[synset_index[synset2]][synset_index[synset1]] = sim
                        #print synset1,sim 
#1 0.0742189207914
#15 0.0442477876106
#17 0.0743000904923
#25 0.0673822870518
     
#     print graph_matrix

    ranked_sense = pr.get_pagerank(graph_matrix, d_factor)
#     print [word for word in words]
    for word in words:
        synsets = word_synsets[word]
        max_r = 0
        max_index = -1
        max_offset = 0
        chosen_synset = None
        for synset in synsets:
            if ranked_sense[synset_index[synset]] >= max_r:
                max_r = ranked_sense[synset_index[synset]]
                #print max_r
                max_offset = synset.offset
                max_index = synset_index[synset]
                chosen_synset = synset
                
                
        rk=searchwl(word_map,word_list,word)
        offset_str=pad_zeros(max_offset)
        answer_line=key[0:3]+" "+rk+" eng-30-"+offset_str+"-"+chosen_synset.pos+"\n"
        f.write(answer_line)
#     print "finished"           
         
if __name__ == '__main__':
    word_map = get_word_map(ENGLISH_xml_path)
    #f1 = open('ENGLISH_RW.answer.test_35','w')
    f2 = open('ENGLISH_RW.answer.test_85','w')
    #f3 = open('ENGLISH_RW.answer.test_90','w')
    tree = etree.parse(ENGLISH_xml_path)
    print "PageRank WSD"
    sentence_map = get_sentence_map(tree)
    #words=['are', 'lessons', 'learnt', 'evaluation', 'mean', 'natural', 'conservation', 'policy']
    
    for key in sentence_map.keys():
        word_list = sentence_map[key].split(",")
#        print word_list
#        print [word_map[word_id] for word_id in word_list]
        
        #process_per_sentence(f1, word_list, word_map, 17, 0.30)
        process_per_sentence(f2, word_list, word_map, 17, 0.85)
        #process_per_sentence(f3, word_list, word_map, 17, 0.90)
#    words1=['church', 'bell', 'rung', 'Sundays']
#    process_per_sentence(words1)
#    
    #f1.close()
    f2.close()
    #f3.close()
    print "finished"