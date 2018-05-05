# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 19:12:08 2018

@author: Foram
"""
import pandas as pd

bi_filename = 'F:/Mtech/Rec Project/Kagel Dataset/books_test_SVD1_900.csv'
ur_filename = 'F:/Mtech/Rec Project/Kagel Dataset/ratings_test_900.csv'




def load_data():
    ############ load data for SVD ############################
    df_rating = pd.read_csv(ur_filename, dtype={'rating': float})
    df_rating=df_rating.drop_duplicates()
    
    
    fields = ['id','book_id','isbn','authors','original_title','title','language_code','average_rating','ratings_count','genres']
    df_book = pd.read_csv(bi_filename,encoding = "ISO-8859-1",dtype={'average_rating': float}, usecols=fields)
    ##################################################
    
    ################ load data for genre_author_based ################
    books={}
    
    for index, row in df_book.iterrows():
        spec = []
        #print(row)
        id_ = row['book_id']
        title = row['original_title']
        authors = row['authors']
        genres = row['genres']
        avg_rating = row['average_rating']
        spec.append(title)
        spec.append(authors)
        spec.append(genres)
        spec.append(avg_rating)
        books[int(id_)] = spec
    
    return(df_rating,df_book,books)
    ###############################################
    
    ################ load data for IISIM_final ###########################
    #fields = ['id','book_id','isbn','authors','original_title','title','language_code','average_rating','ratings_count']
    #books_df = pd.read_csv(bi_filename,dtype={'average_rating': float}, usecols=fields)
    
    ###################################################
    
    ################ get similarbooks by author ###########################
    '''    
    books = {}
    
    alpha =0
    
    
    #df_rating = pd.read_csv(ur_filename, dtype={'rating': float})
    #reader = Reader(rating_scale=(1, 5))
    
    for index, row in df_book.iterrows():
        spec = []
        #print(row)
        id_ = row['book_id']
        title = row['original_title']
        authors = row['authors']
        avg_rating = row['average_rating']
        spec.append(title)
        spec.append(authors)
        spec.append(avg_rating)
        books[int(id_)] = spec
    '''   
    #######################################################################
