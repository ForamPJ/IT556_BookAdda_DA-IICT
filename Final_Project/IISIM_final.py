# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:43:27 2018

@author: Foram
"""

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine, correlation
from scipy import sparse

#------------------
# LOAD THE DATASET
#------------------

dict_topN={}

df_book_local = pd.DataFrame()
df_rating_local = pd.DataFrame()
book_sim_df_local=pd.DataFrame()

bi_filename = 'F:/Mtech/Rec Project/Kagel Dataset/books_test_SVD1_900.csv'
ur_filename = 'F:/Mtech/Rec Project/Kagel Dataset/ratings_test_900.csv'


def get_similar_books( bookid, topN=5):
    #print(bookid)
    df_book['similarity'] = book_sim_df.iloc[bookid-1]
    top_n = df_book.sort_values( ["similarity"], ascending = False )[0:topN]  
    top_n= top_n[top_n.book_id!=bookid]
    spec={}
    for index,row in top_n.iterrows():
        #print(row)
        id_ = row['book_id']
        #title = row['original_title']
        #authors = row['author']
        #similarity = row['similarity']
        if(topN >=4):
            score=1
        elif(topN>2 and topN<=3):
            score=2
        elif(topN==2):
            score=3
        else:
            score=0
        spec[id_]=score
        #spec.append(title)
        #spec.append(authors)
        #spec.append(similarity)
    dict_topN[bookid]=spec
    #top_list = [(book_id,original_title,similarity) for (book_id,original_title,similarity) in top_n]
    #dict_topN[bookid] = top_n
    #print( "Similar Movies to: ", )
    return dict_topN


#def get_book_by_IISIM(df_rating,df_book):
    #df_book_local = df_book
    #df_rating_local = df_rating

df_rating = pd.read_csv(ur_filename, dtype={'rating': float})
df_rating=df_rating.drop_duplicates()
rating_mat = pd.pivot_table(df_rating, index='book_id', columns='user_id', values = "rating" ).reset_index(drop=True)
rating_mat.fillna( 0, inplace = True )
    #rating_mat.head( 10 )
    #data_items = pd.DataFrame(rating_mat)
rating_mat.shape
    
book_sim = 1 - pairwise_distances( rating_mat.as_matrix(), metric="correlation" )
book_sim.shape
book_sim_df = pd.DataFrame( book_sim )
    #book_sim_df.head( 10 )
    #book_sim_df_local =book_sim_df


fields = ['id','book_id','isbn','authors','original_title','title','language_code','average_rating','ratings_count']
df_book = pd.read_csv(bi_filename,dtype={'average_rating': float}, usecols=fields)
        
df_book = df_book.iloc[:,[1,3,4]]
df_book.columns = ['book_id','author','original_title']
    
    #return (df_book , book_sim_df) 
'''
    books_df['similarity'] = book_sim_df.iloc[0]
    books_df.columns = ['book_id', 'title', 'similarity']
    books_df.sort_values( ["similarity"], ascending = False )[1:10]
'''
