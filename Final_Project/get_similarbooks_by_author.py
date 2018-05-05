# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 13:38:27 2018

@author: Foram
"""

import pandas as pd
import numpy as np
from prettytable import PrettyTable
from surprise import Reader

books = {}

alpha =0

bi_filename = 'F:/Mtech/Rec Project/Kagel Dataset/books_test_SVD1_900.csv'
ur_filename = 'F:/Mtech/Rec Project/Kagel Dataset/ratings_test_900.csv'

df_rating = pd.read_csv(ur_filename, dtype={'rating': float})
reader = Reader(rating_scale=(1, 5))

fields = ['id','book_id','isbn','authors','original_title','title','language_code','average_rating','ratings_count']
df_book = pd.read_csv(bi_filename,dtype={'average_rating': float}, usecols=fields)

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

    
def get_title(l):
	return l[0]
def get_author(l):
	return l[1]

'''
Purpose
	get an avg global rating of a book
'''
def get_rating(l):
	return l[2]


'''
Purpose
	get a number of pages of a book
'''
def get_page_num(l):
	return l[1]

'''
Purpose
	get a list of genres of a book
'''
def get_genres(l):
    gen=[]
    genres = l[3].split(';')
    for g in genres:
       gen.append(g.strip())
    #print('genres= ',gen)
    gen= ' '.join(gen).split()
    return gen
	
'''
Purpose
	get a list of sub-genres of a book
'''
def get_sub_genres(l):
    subgen=[]
    sgenres = l[4].split(';')
    for g in sgenres:
       subgen.append(g.strip())
    subgen= ' '.join(subgen).split()
    return subgen

def content_based_recommender(U,n):
    #U=user_responded
    #n=100
    C = {}
    authors_cnt = {}
    total = 0
    #print('U=',U)
    #print('n=',n)
	# calculate a frequency of each genres
    for i in U:
        #i=int(i)
        #print('i =', i)
        loc = get_author(books[i])
        loc =loc.split(',')
        #print('loc=', loc)
        #print('get_authors(books[i])= ',get_author(books[i]))
        
        for content in loc:
            stripped_content = content.strip()
            if stripped_content in authors_cnt:
                #print('content=',content)
                authors_cnt[stripped_content]+=1
            else:
                authors_cnt.setdefault(stripped_content,1.0)
        total+=1
        #print('contents',authors_cnt)
        #print('total',total)
        '''
        for content in contents:
            contents[content] /= total
            print(contents[content])
        '''
    #print('authors_cnt',authors_cnt)
	# build C based on frequency
    
    for j in books:	
        #j_str= j;
        #j= int(j)
        
        loc = get_author(books[j]).split(',')
        #print('loc= ',loc)
        if not(j in U):
            C.setdefault(j,0)
        for content in loc:
            #print('bookid =',j)
            
            stripped_content = content.strip()
            #print('stripped content =',stripped_content)
            if stripped_content in authors_cnt and not(j in U):
                #print('bookid not in U =',j)
                #print('content=',stripped_content)
                #print('contents[content]=',contents[stripped_content])
                C[j]+=authors_cnt[stripped_content]
               # authors_per_book[j].concatanate(stripped_content)
                #print('C[j] =',C[j],'j =', j)
    top_list = [(C[book],book,get_rating(books[book]),get_author(books[book])) for book in C]
    #sorted(top_list,key=lambda x: (x[0],x[2]))
    #top_list.sort()
    #top_list.reverse()	
    top_list = sorted(top_list,key=lambda x: (x[0],x[2]),reverse=True)
    #print('toplist -------------',top_list)
    results = [t for t in top_list if t[0] != 0]
    results =sorted(results,key=lambda x: (x[0],x[2]),reverse=True)
    print('results===================================')
    print(results)
    authors_cnt_desc = sorted(authors_cnt.items(), key=lambda x: x[1], reverse=True)
    return (results[0:n],authors_cnt_desc)
    
			
'''
Purpose
	using the content based recommender and item based recommender,
	pick top n items 
'''	
def topN_recommender(U,n):
    lot,authors_cnt_desc = content_based_recommender(U,100)
    print('lot= ',lot)
    conbook = [i[1] for i in lot]
    print('conbook=',conbook)
    #lot = item_based_recommender(U, conbook)
    #print(lot)
    final_list = conbook
    return (final_list[0:n],lot,authors_cnt_desc)

def get_similar_by_author(user_responded):
    #user_books = []
    #load_data()
    nob=100
    #user_responded = [27, 67, 372, 862, 89]
    #[490,345, 195, 124,18,21]
    lob, list_of_top,authors_cnt_desc = topN_recommender(user_responded,nob)
    df = pd.DataFrame(list_of_top,columns=['count','bookid','rating','author'])
    df_authors_cnt_desc= pd.DataFrame(authors_cnt_desc,columns=['author','count'])
    list_bids=[]
    unique_author_counts =  df_authors_cnt_desc['count'].drop_duplicates().values
    unique_counts = df['count'].drop_duplicates().values
    print(unique_counts)
    if not (set(unique_author_counts) == {1}):
        for count in unique_counts:
            #print('author = ', author)
            print('count = ',count)
            if(count!=1):
                df_ = df.where(df['count'] == count)
                df_auth_cnt = df_authors_cnt_desc.where(df_authors_cnt_desc['count']==count).dropna(thresh=1)
                if df_auth_cnt.empty:
                    if(int(count)>=3):
                        df_trunc = df_.dropna(thresh=1).head(3)
                        print(df_trunc)
                        a = np.int_(df_trunc['bookid'].values)
                        print(a.tolist())
                        list_bids.extend(a)
                        print('list_bids========',list_bids)
                    elif(int(count)<3 and int(count)>=2):
                        df_trunc = df_.dropna(thresh=1).head(int(count))
                        print(df_trunc)
                        a=np.int_(df_trunc['bookid'].values)
                        print(a.tolist())
                        list_bids.extend(a)
                        print('list_bids========',list_bids)
                    else:
                        print('nothing')
                else:
                    for index,row in df_auth_cnt.iterrows():
                        auth = row['author']
                        print('author ---->>>',auth)
                        df_per_auth_cnt = df_[df_['author'].str.contains(auth)==True]
                        print('df_per_auth_cnt =========',df_per_auth_cnt)
                        if(int(count)>=3):
                            df_trunc = df_per_auth_cnt.dropna(thresh=1).head(3)
                            print(df_trunc)
                            a = np.int_(df_trunc['bookid'].values)
                            print(a.tolist())
                            list_bids.extend(a)
                            print('list_bids========',list_bids)
                        elif(int(count)<3 and int(count)>=2):
                            df_trunc = df_per_auth_cnt.dropna(thresh=1).head(int(count))
                            print(df_trunc)
                            a=np.int_(df_trunc['bookid'].values)
                            print(a.tolist())
                            list_bids.extend(a)
                            print('list_bids========',list_bids)
                        else:
                            print('no proper author pattern')
                        #df.groupby('count').head(2).where(df['count'] == 3.0)
            
        
        print ('::: Top {0} recommendation System:::' .format(nob))
        print ('*User browsed books:')
        n=1
        for ids in user_responded:
            ids =int(ids)
    		#for test purpose only: comment out
    		#print ids, get_title(books[ids])
            #loc = get_genres(books[ids])+get_sub_genres(books[ids])
            print( '{0}. {1}. by [{2}]. ({3})'.format(n,get_title(books[ids]),get_author(books[ids]),get_rating(books[ids])))
            #print(get_title(books[ids]))
            #print(loc)
            n=n+1;
        print (' ')
        print ('*Recommended books: ')
        n=1
        for ids in list_bids:
            ids = int(ids)
    		#for test purpose only: comment out
    		#print '{0}. {1}, {2}'.format(n, get_title(books[ids]), ids)
            #loc = get_genres(books[ids])+get_sub_genres(books[ids])
            print( '{0}. book ID = {1} {2}. by [{3}]. ({4})'.format(n,ids,get_title(books[ids]),get_author(books[ids]),get_rating(books[ids])))
            #print( '{0}. {1}. {2}'.format(n, get_title(books[ids]),loc))
            n+=1
            
        return(list_bids)
