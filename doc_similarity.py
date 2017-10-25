from query_reweighting import unpickleDictionary,tf_idf_query
from word_similarity import wup_sim
from sys import argv
import numpy as np

def cartesian(a,b,op='product'):
    if op == 'product':
        return np.tile(b,len(a))*np.tile(a,len(b))
    else:
        return np.array([wup_sim(w1,w2) for w1 in a for w2 in b])

def cartesian_2(a,b):
    for k1 in a:
        for k2 in b:
            if b[k2] > 0.1:
                print k1,k2,'\t\t', b[k2]
                print wup_sim(k1,k2)


if __name__ == '__main__':
    query = raw_input("Enter a query:\n").lower()
    terms = query.split()
    idf = unpickleDictionary('idf.txt')
    print 'dictionary unpickled'
    q_d = tf_idf_query(terms, idf)

    docs_tf_idf = unpickleDictionary('tf_idf.txt')

    qk = np.array(list(q_d.keys()))
    qv = np.array(list(q_d.values()))

    while True:
        doc = raw_input("Enter document name\n")
        if doc[-4:] != '.txt':
            print 'Enter a valid path'
            continue
        print doc

        d_d = docs_tf_idf[doc]
        dk = np.array(list(d_d.keys()))
        dv = np.array(list(d_d.values()))


        # cartesian_2(q_d,d_d)

        similarities = cartesian(qk,dk,'sim')
        # print similarities
        product = cartesian(qv,dv,'product')
        # print product

        num = sum(product*similarities)
        den = sum(product)
        if den != 0:
            result = num/den
        else:
            result = 0
        print result
