# -*- coding: utf-8 -*-

import spacy
import en_core_web_sm
import pandas as pd
nlp = en_core_web_sm.load()

df = pd.read_csv('C:\\Users\\student\\Downloads\\BXCSVDump\\BX-Books2.csv')
#df['text_as_spacy_title'] = df['Book-Title'].apply(nlp)
print(df['Book-Title'])

'''
doc = nlp('am is are eat ate eaten car cars car''s cars'' god''s ')

for token in doc:
        print(token.text, token.lemma_)
'''
        
for item in df['Book-Title']:
    #item.replace("'","''")
   # print(item)
    doc = nlp(item)
    #print(doc)
    for ent in doc.ents:
        print(ent.text,  '|',ent.label_)

'''
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)
'''
