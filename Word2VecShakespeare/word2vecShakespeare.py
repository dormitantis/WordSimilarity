# coding=utf-8

import string
import pymorphy2
import re
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

morph = pymorphy2.MorphAnalyzer()
punctuation = re.compile('[\\d\\{}]'.format("\\".join(string.punctuation)))

string = open('shakespeare.txt', 'r').read()
string = (unicode(string, encoding='utf-8')). \
    replace('x x x', '\n'). \
    replace('\n', ' '). \
    replace('?', '.'). \
    replace('!', '.'). \
    replace('. ', '\n')

listSentences = string.split('\n')

editedSonets = list()
for line in listSentences:
    wordList = list()
    for part in punctuation.sub("", line).split():
        mo = morph.parse(part)
        if mo:
            word = mo[0]
            if word.tag.POS not in ("NUMR", "PREP", "CONJ", "PRCL", "INTJ"):
                wordList.append(word.normal_form)
    editedSonets.append(wordList)

model = gensim.models.Word2Vec(editedSonets, min_count=5, size=100)

similarity = model.most_similar(positive=[u'любовь'], topn=50)
for each in similarity:
    mo = morph.parse(each[0])
    if mo:
        word = mo[0]
        if word.tag.POS in ("NOUN"):
            print each[0], each[1]
