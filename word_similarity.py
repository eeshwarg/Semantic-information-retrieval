from nltk.corpus import wordnet as wn
from itertools import product

def wup_sim(word1, word2):
    w1 = wn.synsets(word1)
    w2 = wn.synsets(word2)
    set1 = set(ss for ss in w1)
    set2 = set(ss for ss in w2)
    if(set1 and set2):
        best = max((wn.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(set1, set2))
        return best[0]
    return 0
