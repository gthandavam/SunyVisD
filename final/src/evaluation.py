import math
import re
import sqlite3
from nltk import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
from time import time

DB_PATH = 'E:/Desktop/wikiprep/tfidf-d80-t2.5-indexed-tfidf-desc.db'
CONCEPT_LIMIT = 10

conn = sqlite3.connect(DB_PATH)
sql = conn.cursor()
punc_rx = re.compile(r'[^A-Za-z0-9]+', re.DOTALL)
no_of_docs = 1857524
stemmer = PorterStemmer()
stem = lambda w: stemmer.stem(stemmer.stem(stemmer.stem(w))) # stem three times
stop = sw.words('english')

def cosine_similarity(v1, v2):
    ret  = 0
    den1 = 1
    den2 = 1
    for key in range(no_of_docs):
        if key in v1:
            den1 += v1[key] * v1[key]
        if key in v2:
            den2 += v2[key] * v2[key]
        if key in v1 and key in v2:    
            ret += v1[key] * v2[key]
#    print den1, den2
    return ret/(math.sqrt(den1) * math.sqrt(den2))

#assume context word only text

def get_word_tfidf(word):
    ret = {}
    for row in sql.execute("SELECT word, concept_id, tfidf from inverted_index "+
         "ii join words w on ii.word_id = w.id WHERE w.word = '"+word+"'  LIMIT "+
         str(CONCEPT_LIMIT)+";"):
        ret[row[1]] =  row[2]
    return ret

def get_text_tfidf(words):
    vs = {}
    for word in words:
        vs[word] = get_word_tfidf(word)
    ret = {}
    for concept in range(no_of_docs):
        val = 0
        for word in vs.keys():
                if concept in vs[word]:
                    val += vs[word][concept]
        if(val):
            ret[concept] = val
    
    return ret 

def cleanse_text(text):
    text = re.sub(punc_rx, ' ', text)
    ret = []
    for word in text.split():
        if(word not in stop):
            ret.append(stem(word))
    return ret

if __name__ == '__main__':
    
#    text = "Obama deliver his first speech."
#
#    sent  =  nltk.sent_tokenize(text)
#    
#    
#    print sent
#
#    loftags = []
#    for s in sent:
#        if(s not in sw.words('english')):
#            d = nltk.word_tokenize(s)   
#    
#            pos_s = nltk.pos_tag(d)
#            print pos_s[1][0]
#            print pos_s[1][1]
#            
#            print wn.synsets(pos_s[1][0], 'v')
#            print sw.words('english')
    
#    v1 = { 0 : 2, 1 : 0 } ;
#    v2 = { 0 : 1, 2 : 2 } ;
#    print cosine_similarity(v1, v2)
    print "for hot dog gourmet"
    t1 = time()
    v1 = get_text_tfidf(cleanse_text('hot dog gourmet'))
    t2 = time()
    print t2-t1
#    
#    print "synsets for dog"
#    
#    
#    t1 = time()
#    v2 = get_text_tfidf('dog')
#    t2 = time()
#    print t2-t1
#    
#    print v1
#    print v2
#    print cosine_similarity(v1, v2)
#    
    cand_list = {} 
    
    print "for dog synsets"
    t1 = time()
    for lemma in wn.lemmas('dog'):
        #print (wn.synset(synset).definition)
        cand_list[lemma] = get_text_tfidf(cleanse_text(lemma.synset.definition))
    t2 = time()
    print t2-t1
    
    max_lemma = None
    max_sim = -1;
    for key in cand_list.keys():
        sim = cosine_similarity(v1, cand_list[key])
        if ( sim > max_sim ):
            max_lemma = key
            max_sim = sim
    
    print "max sim score and the lemma"
    print max_sim;
    print max_lemma.synset.definition;
    print max_lemma.synset 
    print "for snail"
    t1 = time()
    print get_text_tfidf('snail')
    t2 = time()
    print t2-t1

    conn.close()
    
    
    
    