
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import spacy
import en_core_web_sm
import pandas as pd
nlp = en_core_web_sm.load()

df= pd.read_csv('C:\\Users\\student\\Desktop\\mausamee\\bx-books-test-1.csv')

for token in doc:
    print(token.text, token.lemma_)

for item in df['Book-Title']:
    doc=nlp(item)
    #print(doc)
    for token in doc:
        print(token.text, token.lemma_)


for item1 in df['Publisher']:
    doc=nlp(item1)
    #print(doc)
    for token in doc:
        print(token.text, token.lemma_)
