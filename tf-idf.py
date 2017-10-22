from __future__ import division
from nltk.tokenize import RegexpTokenizer
from sys import argv
import cPickle
from collections import defaultdict
import os
import math

input_dir = argv[1]

tf_in_docs = {}
tf_idf = {}
df = defaultdict(int)

tokenizer = RegexpTokenizer(r'\w+')

def pickleDictionary(dict,file):
    with open(file,'wb') as f:
        cPickle.dump(dict,f)
    f.close()

def index_doc(file):
    doc = {}
    no_of_words = 0
    with open(input_dir+file,'r') as f:
        for line in f:
            for word in tokenizer.tokenize(line.decode('utf8')):
                word = word.lower()
                no_of_words += 1
                if word not in doc:
                    doc[word] = 1
                    df[word] += 1
                else:
                    doc[word] += 1
    f.close()
    for word in doc:
        doc[word] = doc[word]/no_of_words

    tf_in_docs[file] = doc

for file in os.listdir(input_dir):
    if file.endswith(".txt"):
        index_doc(file)

no_of_docs = len(tf_in_docs)
idf = {}
for key in df:
    idf[key] = math.log(no_of_docs/df[key])

for doc in tf_in_docs:
    t = tf_in_docs[doc]
    tf_idf[doc] = {}
    for word in t:
        tf_idf[doc][word] = t[word] * idf[word]

pickleDictionary(tf_idf,'tf_idf.txt')
pickleDictionary(idf,'idf.txt')
