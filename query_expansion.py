from __future__ import division
import query_reweighting as qr
import nltk
from nltk.corpus import brown, wordnet as wn
from word_similarity import wup_sim

THRESHOLD = 0.8
freq = []

def equals(a,b):
    if type(a) == type(b):
        return a==b
    elif type(a) is nltk.corpus.reader.wordnet.Synset:
        return (a.name().split(".")[0]) == b
    else:
        return a == (b.name().split('.')[0])

def get_most_common_sense(word):
    common = 'n'
    max_count = freq['NOUN'][word]
    if freq['VERB'][word] > max_count:
        common = 'v'
        max_count = freq['VERB'][word]
    elif freq['ADJ'][word] > max_count:
        common = 'a'
        max_count = freq['ADJ'][word]
    elif freq['ADV'][word] > max_count:
        common = 'r'
        max_count = freq['ADV'][word]

    return common

def get_hyper_or_hyponyms(word,type='hypo'):
    pos = get_most_common_sense(word)
    l = []
    try:
        w = wn.synset(word+'.'+pos+'.1')
        if type == 'hypo':
            nym = w.hyponyms()
        else:
            nym = w.hypernyms()
        # print nym
        l.append(w)
        for h in nym:
            # print w,h,wup_sim(w,h)
            if wup_sim(w,h) > THRESHOLD:
                l.append(h)
    except:
        # do some shit
        print 'Word not present in wordnet'
    return l

# term_weights is a dictionary of the form synset/word: (weight, number of hyponyms, boolean indicating whether hypernym was added)
def reweight_terms(term_weights):
    new_dict = {}
    for t1 in term_weights:
        extra = 0
        for t2 in term_weights:
            sim = wup_sim(t1,t2)
            if not equals(t1,t2) and sim>THRESHOLD and term_weights[t2][1] > 0:
                extra += term_weights[t2][0] * sim / term_weights[t2][1]
            if term_weights[t2][2]:
                extra += term_weights[t2][0] * sim
        term_weights[t1][0] += extra
        if type(t1) is nltk.corpus.reader.wordnet.Synset:
            new_dict[t1.name().split(".")[0].replace('_',' ')] = term_weights[t1][0]
        else:
            new_dict[t1] = term_weights[t1][0]

    return new_dict

if __name__ == '__main__':
    freq = nltk.ConditionalFreqDist((tag, wrd.lower()) for wrd, tag in brown.tagged_words(tagset="universal"))
    while True:
        # word = raw_input("Enter a word for which you want hypernyms and hyponyms\n")
        # print 'Hyponyms:'
        # print 'Hypernyms:'


        query = raw_input("Enter a query\n  ")
        terms = query.split()
        idf = qr.unpickleDictionary('idf.txt')
        q = qr.tf_idf_query(terms,idf)
        q_dash = qr.reweight(terms,q)
        print q_dash

        term_weights = {}
        for word in q_dash:
            hypo = get_hyper_or_hyponyms(word,'hypo')
            print 'hypo:', hypo
            print
            hyper = get_hyper_or_hyponyms(word,'hyper')
            print 'hyper:', hyper
            print
            if len(hypo) > 0:
                had_hyper = True if len(hyper) > 1 else False
                term_weights[hypo[0]] = [q_dash[word],len(hypo)-1,had_hyper]
                for i in range(1,len(hypo)):
                    term_weights[hypo[i]] = [0,0,False]
                for i in range(1,len(hyper)):
                    term_weights[hyper[i]] = [0,0,False]
            else:
                term_weights[word] = [0,0,False]


        # print term_weights

        reweighted_query = reweight_terms(term_weights)

        min = float('inf')
        max = -1*min
        for word in reweighted_query:
            if reweighted_query[word] < min:
                min = reweighted_query[word]
            elif reweighted_query[word] > max:
                max = reweighted_query[word]

        f = open('modified_query.txt','w')
        for word in reweighted_query:
            f.write(word + '\t' + str((reweighted_query[word]-min)/(max-min)) + '\n')
        f.close()
