import nltk
from nltk.corpus import wordnet as wn
from itertools import product

def not_found(a,b):
    if type(a) is nltk.corpus.reader.wordnet.Synset:
        a = a.name().split(".")[0]
    if type(b) is nltk.corpus.reader.wordnet.Synset:
            b = b.name().split(".")[0]
    if a == b:
        return 1
    return 0

def wup_sim(word1, word2):
    if type(word1) is type(word2) and type(word1) is nltk.corpus.reader.wordnet.Synset:
        return wn.wup_similarity(word1,word2)
    if type(word1) is str:
        w1 = wn.synsets(word1)
    elif type(word1) is nltk.corpus.reader.wordnet.Synset:
        w1 = []
        w1.append(word1)
    if type(word2) is str:
        w2 = wn.synsets(word2)
    elif type(word2) is nltk.corpus.reader.wordnet.Synset:
        w2 = []
        w2.append(word2)
    print type(word1)
    set1 = set(ss for ss in w1)
    set2 = set(ss for ss in w2)
    if(set1 and set2):
        best = max((wn.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(set1, set2))
        return best[0]
    return not_found(word1,word2)

if __name__ == '__main__':
    w1 = wn.synsets('dog')[0]
    w2 = wn.synsets('cat')[0]
    print wup_sim(w1,w1)
