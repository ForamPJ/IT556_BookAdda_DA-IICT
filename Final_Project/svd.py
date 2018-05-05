# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 09:09:39 2018

@author: Foram
"""

from collections import defaultdict
import time
from surprise import SVD
from surprise import Dataset
from prettytable import PrettyTable
from surprise import Reader


def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''
    #to get the ratings for id = 1
    ''' 
    id_1 = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        if(uid == 1):
            id_1[uid].append((iid, est))

    for uid,iid  in id_1.items():
        iid.sort(key=lambda x: x[0], reverse=False)
        id_1[uid] = iid[:]
    '''
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def train_test_svd(userx,df_rating,df_book):
    # First train an SVD algorithm on the movielens dataset.
    #data = Dataset.load_builtin('ml-100k')
    
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_rating[['user_id','book_id','rating']], reader)
    df_distinct_rating = df_rating.drop_duplicates(['user_id', 'book_id', 'rating'])
    #R= df_distinct_rating.pivot(index = 'user_id', columns ='book_id', values = 'rating').fillna(0).to_sparse(fill_value=0)
    
    
    
    #reader = Reader(rating_scale=(1, 5))
    #data_book = Dataset.load_from_df(df_book[['id','book_id','isbn','authors','original_title','title','language_code','average_rating','ratings_count']],reader)
    
    
    #noofbooks_ratedbyUser = df_distinct_rating.groupby('user_id')['rating'].count()
    #books_ratedbynoofUser = df_distinct_rating.groupby('book_id')['rating'].count()
    
    #books rated by users
    df_rated = df_distinct_rating
    #userx=377
    user_data=df_rated[df_rated['user_id']==userx]
    #non_rated_data=user_data[user_data['rating']==float('NaN')]
    t = PrettyTable(['Book Id', 'Title' ])
    print("********************************************************")
    print("Rated Items By User")
    print("********************************************************")
    for index, row in user_data.iterrows():
        #print(row)
        id_=int(row['book_id'])
        book_detail= df_book[df_book.id == id_]
        r =[]
        r.append(int(row['book_id']))
        r.append(book_detail['original_title'].values[0])
        t.add_row(r)
        #print("Book ID = ", row['book_id'])
        #print("Book Title = ", book_detail['title'])
        
    print(t)
    #trainset, testset = train_test_split(data, test_size=.25)
    
    trainset = data.build_full_trainset()
    start = time.time() 
    algo = SVD()
    algo.fit(trainset)
    end = time.time()
    print('total time taken for training is =', end-start)
    
    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    start = time.time()
    testset = trainset.build_anti_testset()
    end = time.time()
    print('total time taken for creating train set is =', end-start)
    
    
    start = time.time() 
    predictions = algo.test(testset)
    end = time.time()
    print('total time taken for prdiction is =', end-start)
    
    
    start = time.time() 
    top_n = get_top_n(predictions, n=10)
    end = time.time()
    print('total time taken for top 10 recommendation is =', end-start)
    
    return top_n
    
    
    
