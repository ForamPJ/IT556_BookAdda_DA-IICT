# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 18:43:26 2018

@author: Mausamee Patel
"""

import numpy as np
import pandas as pd
import csv
import sklearn.preprocessing as sk
from gensim.corpora import MmCorpus
from gensim.test.utils import get_tmpfile
import gensim
import gensim.models.lsimodel as ls

from sklearn.decomposition import TruncatedSVD
from sklearn.random_projection import sparse_random_matrix
from sklearn.utils.extmath import randomized_svd

ratings_df = pd.read_csv('C:/Users/Mausamee Patel/Desktop/Project/A4/finalcodefor1milliondata/ratings_1million.csv', dtype={'rating': float})
print (ratings_df)
print (ratings_df.head())
ratings_df.loc[:,'rating'] = sk.minmax_scale(ratings_df.loc[:,'rating'] )
print(ratings_df.loc[:,'rating'])
print (ratings_df)
print (ratings_df.head())


R_df = ratings_df.pivot(index = 'user_id', columns ='book_id', values = 'rating').fillna(0).to_sparse(fill_value=0)
print(R_df.head())

R = R_df.as_matrix()
if(np.isinf(R).all()==False):
    print("tr")
##print(np.isinf(R),np.isnan(R))

Z=gensim.matutils.Dense2Corpus(R, documents_columns=True)
print(Z)

##user_ratings_mean = np.mean(R, axis = 1)
#print(R.size)
lsi=ls.LsiModel(Z, num_topics=3)
print("Sigma")

print(lsi.projection.s)
print("U")

print(lsi.projection.u)
print("VT")
V = gensim.matutils.corpus2dense(lsi[Z], len(lsi.projection.s)).T / lsi.projection.s
print(V)

