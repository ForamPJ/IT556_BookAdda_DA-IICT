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
import psutil

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
mem=[]
m1=psutil.virtual_memory().percent


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
m2=psutil.virtual_memory().percent
#print(m2)
mem.append(m2)

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
m3=psutil.virtual_memory().percent
#print(m2)
mem.append(m3)


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
m4=psutil.virtual_memory().percent
#print(m2)
mem.append(m4)


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
m5=psutil.virtual_memory().percent
#print(m2)
mem.append(m5)


#plot time
y = [len(df1),len(df2),len(df3),len(df4)]
plt.plot( timex[0],y[0],'ro',label='100 records')
plt.plot( timex[1], y[1],'bo',label='1000 records')
plt.plot( timex[2],y[2],'go',label='10000 records')
plt.plot( timex[3], y[3],'yo',label='100000 records')
legend = plt.legend(loc='upper left',bbox_to_anchor=(1, 1))
frame = legend.get_frame()
plt.xlabel('Time(in sec)')
plt.ylabel('Number of records')
plt.title('Time Vs Number of Records')

plt.show()


#plot mean rmse
y = [len(df1),len(df2),len(df3),len(df4)]
plt.plot( np.mean(result1['rmse']),y[0],'gs',label='100 records')
plt.plot( np.mean(result2['rmse']),y[1],'rs',label='1000 records')
plt.plot( np.mean(result3['rmse']),y[2],'bs',label='10000 records')
plt.plot( np.mean(result4['rmse']),y[3],'ys',label='100000 records')
legend = plt.legend(loc='upper left',bbox_to_anchor=(1, 1))
frame = legend.get_frame()
plt.xlabel('Mean RMSE')
plt.ylabel('Number of records')
plt.title('Mean RMSE Vs Number of Records')
plt.show()

#memory usage
y = [len(df1),len(df2),len(df3),len(df4)]
plt.plot( mem[0],y[0],'g^',label='100 records')
plt.plot( mem[1],y[1],'r^',label='1000 records')
plt.plot( mem[2],y[2],'b^',label='10000 records')
plt.plot( mem[3],y[3],'y^',label='100000 records')
legend = plt.legend(loc='upper left',bbox_to_anchor=(1, 1))
frame = legend.get_frame()
plt.xlabel('% of Memory Usage')
plt.ylabel('Number of records')
plt.title('% of Memory Usage Vs Number of Records')
plt.show()

