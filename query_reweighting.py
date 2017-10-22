from __future__ import division
import itertools
from collections import defaultdict
from word_similarity import wup_sim
import cPickle

THRESHOLD = 0.8

query = raw_input("Enter a query\n  ")

terms = query.split()

def unpickleDictionary(file):
    with open(file,'rb') as f:
        retrievedDict = cPickle.load(f)
    f.close()

    return retrievedDict

def tf_idf_query(terms,idf):
    d_terms = defaultdict(int)
    for term in terms:
        d_terms[term] += 1

    for term in d_terms:
        try:
            d_terms[term] *= idf[term]
        except:
            d_terms[term] = 0

    return d_terms

def reweight(terms, q):
    q_dash = q.copy()
    for i in range(len(terms)):
        for j in range(i+1,len(terms)):
            sim = wup_sim(terms[i],terms[j])
            print sim
            if(sim > THRESHOLD):
                q_dash[terms[i]] += q[terms[j]]*sim
                q_dash[terms[j]] += q[terms[i]]*sim
    return q_dash

idf = unpickleDictionary('idf.txt')
q = tf_idf_query(terms,idf)
q_dash = reweight(terms,q)

print q
print q_dash
