import spacy
import en_core_web_sm
import pandas as pd
nlp = en_core_web_sm.load()

df = pd.read_csv('C:\\Users\\dell pc\\Desktop\\Project\\BX-BookData_new.csv')
print("\n        For BOOK TITLE    \n")
     
for item in df['Book-Title']:
    doc = nlp(item)
    #print(doc)
    for ent in doc.ents:
        print(ent.text,  '|',ent.label_)
        
print("\n        For PUBLISHERS    \n")  

for item in df['Publisher']:
    doc = nlp(item)
    #print(doc)
    for ent in doc.ents:
        print(ent.text,  '|',ent.label_)

print("\n        For GENRE    \n")

for item in df['Genre']:
    doc = nlp(item)
    #print(doc)
    for ent in doc.ents:
        print(ent.text,  '|',ent.label_)
