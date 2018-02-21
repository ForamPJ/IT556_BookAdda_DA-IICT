import spacy
import en_core_web_sm
import pandas as pd

nlp = en_core_web_sm.load()

df= pd.read_csv('C:\\Users\\dell pc\\Desktop\\Project\\BX-BookData_new.csv')

print("\n        For BOOK TITLE    \n")
for item in df['Book-Title']:
    doc=nlp(item)
    #print(doc)
    for token in doc:
        print(token.text, token.lemma_)

print("\n        For PUBLISHERS    \n")  
for item1 in df['Publisher']:
    doc=nlp(item1)
    #print(doc)
    for token in doc:
        print(token.text, token.lemma_)

print("\n        For GENRE    \n")
for item1 in df['Genre']:
    doc=nlp(item1)
    #print(doc)
    for token in doc:
        print(token.text, token.lemma_)
