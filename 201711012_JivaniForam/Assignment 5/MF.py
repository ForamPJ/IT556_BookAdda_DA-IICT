# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:04:54 2018

@author: IIRAMII
"""

import numpy as np
import surprise
import pandas as pd
from surprise import Reader
from surprise import Dataset
import time
import matplotlib.pyplot as plt


class MatrixFacto(surprise.AlgoBase):
    '''A basic rating prediction algorithm based on matrix factorization.'''
    skip_train=0
    
    def __init__(self, learning_rate, n_epochs, n_factors):
        
        self.lr = learning_rate  # learning rate for SGD
        self.n_epochs = n_epochs  # number of iterations of SGD
        self.n_factors = n_factors  # number of factors
        
    def train(self, trainset):
        '''Learn the vectors p_u and q_i with SGD'''
        
        print('Fitting data with SGD...')
        
        # Randomly initialize the user and item factors.
        p = np.random.normal(0, .1, (trainset.n_users, self.n_factors))
        q = np.random.normal(0, .1, (trainset.n_items, self.n_factors))
        
        # SGD procedure
        for _ in range(self.n_epochs):
            for u, i, r_ui in trainset.all_ratings():
                err = r_ui - np.dot(p[u], q[i])
                # Update vectors p_u and q_i
                p[u] += self.lr * err * q[i]
                q[i] += self.lr * err * p[u]
                # Note: in the update of q_i, we should actually use the previous (non-updated) value of p_u.
                # In practice it makes almost no difference.
        
        self.p, self.q = p, q
        self.trainset = trainset

    def estimate(self, u, i):
        '''Return the estmimated rating of user u for item i.'''
        
        # return scalar product between p_u and q_i if user and item are known,
        # else return the average of all ratings
        if self.trainset.knows_user(u) and self.trainset.knows_item(i):
            return np.dot(self.p[u], self.q[i])
        else:
            return self.trainset.global_mean
        
timex=[]

start = time.time()
df1 = pd.read_csv('C:/Users/Foram/Desktop/Project/ratings_1million1.csv', dtype={'rating': float})
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df1[['user_id','book_id','rating']], reader)
data.split(2)
algo = MatrixFacto(learning_rate=.01, n_epochs=10, n_factors=10)
result1 = surprise.evaluate(algo, data, measures=['RMSE'])
end = time.time()
print("Time1",end - start)
timex.append(end-start)


start = time.time()
df2 = pd.read_csv('C:/Users/Foram/Desktop/Project/ratings_1million2.csv', dtype={'rating': float})
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df2[['user_id','book_id','rating']], reader)
data.split(2)
algo = MatrixFacto(learning_rate=.01, n_epochs=10, n_factors=10)
result2 = surprise.evaluate(algo, data, measures=['RMSE'])
end = time.time()
print("Time2",end - start)
timex.append(end-start)


start = time.time()
df3 = pd.read_csv('C:/Users/Foram/Desktop/Project/ratings_1million3.csv', dtype={'rating': float})
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df3[['user_id','book_id','rating']], reader)
data.split(2)
algo = MatrixFacto(learning_rate=.01, n_epochs=10, n_factors=10)
result3 = surprise.evaluate(algo, data, measures=['RMSE'])
end = time.time()
print("Time3",end - start)
timex.append(end-start)


start = time.time()
df4 = pd.read_csv('C:/Users/Foram/Desktop/Project/ratings_1million4.csv', dtype={'rating': float})
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df4[['user_id','book_id','rating']], reader)
data.split(2)
algo = MatrixFacto(learning_rate=.01, n_epochs=10, n_factors=10)
result4 = surprise.evaluate(algo, data, measures=['RMSE'])
end = time.time()
print("Time4",end - start)
timex.append(end-start)

#plot time
y = [len(df1),len(df2),len(df3),len(df4)]
plt.plot( timex[0],y[0], 'r^', timex[1], y[1],'bs', timex[2],y[2],'g^',timex[3], y[3],'gs')
plt.show()

#plot mean rmse
y = [len(df1),len(df2),len(df3),len(df4)]
plt.plot( np.mean(result1['rmse']),y[0], 'r^', np.mean(result2['rmse']), y[1],'bs', np.mean(result3['rmse']),y[2],'g^',np.mean(result4['rmse']), y[3],'gs')
plt.show()

#memory usage

