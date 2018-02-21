import spacy
import en_core_web_sm
import pandas as pd

nlp = en_core_web_sm.load()

df = pd.read_csv('C:\\Users\\dell pc\\Desktop\\Project\\BX-BookData_new.csv')
df1 = df['Book-Title'].apply(nlp)
for temp in df1:
        for chunk in temp.noun_chunks:
          print(chunk.root.text)
print("\n")
          
df2 = df['Publisher'].apply(nlp)
for temp in df2:
        for chunk in temp.noun_chunks:
          print(chunk.root.text)
print("\n")

df3 = df['Genre'].apply(nlp)
for temp in df3:
        for chunk in temp.noun_chunks:
          print(chunk.root.text)

          
