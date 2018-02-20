import spacy
import en_core_web_sm
import csv
import pandas as pd

nlp = en_core_web_sm.load()



df = pd.read_csv('bx-books-test-1.csv')
df1 = df['Book-Title'].apply(nlp)
#print(df['text_spacy_title'])

for temp in df1:
        for chunk in temp.noun_chunks:
          print(chunk.root.text)

        print("\n")
          
