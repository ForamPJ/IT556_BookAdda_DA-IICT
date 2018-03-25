# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 23:29:40 2018

@author: IIRAMII
"""

import numpy as np
import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import Reader
import time
import matplotlib.pyplot as plt
start = time.time()

import psutil
import os


x=[]
timex=[]
mem=[]



process=psutil.Process(os.getpid())
m1=psutil.virtual_memory().percent
print(m1)    
print(psutil.virtual_memory())
  
df1 = pd.read_csv('D:\\DA Sem2\\Recommandation System\\Lab 6\\ratings_1million1.csv', dtype={'rating': float})
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df1[['user_id','book_id','rating']], reader)
algo = SVD()
result1=cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)
#print(result1)
x.append(np.mean(result1['test_rmse']))
end = time.time()
#print("Time1",end - start)
timex.append(end-start)
#process=psutil.Process(os.getpid())
m2=psutil.virtual_memory().percent
#print(m2)
mem.append(m2)

print(psutil.virtual_memory())


start = time.time()
df2 = pd.read_csv('D:\\DA Sem2\\Recommandation System\\Lab 6\\ratings_1million2.csv', dtype={'rating': float})
data = Dataset.load_from_df(df2[['user_id','book_id','rating']], reader)
result2=cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)
#print(result2)
x.append(np.mean(result2['test_rmse']))
end = time.time()
#print("Time2",end - start)
timex.append(end-start)
#process=psutil.Process(os.getpid())
m3=psutil.virtual_memory().percent

#print(m3)
mem.append(m3)


start = time.time()
df3 = pd.read_csv('D:\\DA Sem2\\Recommandation System\\Lab 6\\ratings_1million3.csv', dtype={'rating': float})
data = Dataset.load_from_df(df3[['user_id','book_id','rating']], reader)
result3=cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)
#print(result3)
x.append(np.mean(result3['test_rmse']))
end = time.time()
#print("Time3",end - start)
timex.append(end-start)
#process=psutil.Process(os.getpid())
m4=psutil.virtual_memory().percent
#print(m4)
mem.append(m4)


start = time.time()
df4 = pd.read_csv('D:\\DA Sem2\\Recommandation System\\Lab 6\\ratings_1million4.csv', dtype={'rating': float})
data = Dataset.load_from_df(df4[['user_id','book_id','rating']], reader)
result4=cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)
#print(result4)
x.append(np.mean(result4['test_rmse']))
end = time.time()
#print("Time4",end - start)
timex.append(end-start)
#process=psutil.Process(os.getpid())
m5=psutil.virtual_memory().percent
#print(m5)
mem.append(m5)
 



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


y = [len(df1),len(df2),len(df3),len(df4)]
plt.plot( x[0],y[0],'gs',label='100 records')
plt.plot( x[1],y[1],'rs',label='1000 records')
plt.plot( x[2],y[2],'bs',label='10000 records')
plt.plot( x[3],y[3],'ys',label='100000 records')
legend = plt.legend(loc='upper left',bbox_to_anchor=(1, 1))
frame = legend.get_frame()
plt.xlabel('Mean RMSE')
plt.ylabel('Number of records')
plt.title('Mean RMSE Vs Number of Records')
plt.show()



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




