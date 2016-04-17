__author__ = 'aliHitawala'

import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
print wn.synsets('dog')
# wn.synsets('dog', pos=wn.VERB)
# nltk.download()
# sorted(wn.langs())
print brown.words()