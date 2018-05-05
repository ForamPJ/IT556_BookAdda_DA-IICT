# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:51:21 2018

@author: Foram
"""

import pandas as pd

books={}
bi_filename = 'F:/Mtech/Rec Project/Kagel Dataset/books_test_SVD1_900.csv'

fields = ['id','book_id','isbn','authors','original_title','title','language_code','average_rating','ratings_count','genres']
books_df = pd.read_csv(bi_filename,encoding = "ISO-8859-1",dtype={'average_rating': float}, usecols=fields)

for index, row in books_df.iterrows():
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

def get_title(l):
	return l[0]

def get_genres(l):
    gen=[]
    if not (pd.isnull(l[2])):
        genres = l[2].split(';')
        for g in genres:
           gen.append(g.strip())
        #print('genres= ',gen)
        gen= ' '.join(gen).split()
        
    return gen

def get_author(l):
	return l[1]


def get_list_gen(x):
    gen=[]
    if not (pd.isnull(x)):
        genres = x.split(';')
        for g in genres:
           gen.append(g.strip())
        #print('genres= ',gen)
        gen= ' '.join(gen).split()
    #names = [i['name'] for i in x]
    #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
    #if len(names) > 3:
     #   names = names[:3]
     #   return names

    #Return empty list in case of missing/malformed data
    return gen

def get_list_auth(x):
    auth=[]
    if not (pd.isnull(x)):
        authors = x.split(',')
        for g in authors:
           auth.append(g.strip())
        #print('genres= ',gen)
        auth= ' '.join(auth).split()
    #names = [i['name'] for i in x]
    #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
    #if len(names) > 3:
     #   names = names[:3]
     #   return names

    #Return empty list in case of missing/malformed data
    return auth


books_df['authors'] = books_df['authors'].apply(get_list_auth)
books_df['genres'] = books_df['genres'].apply(get_list_gen)
books_df['authors'].head(3)
books_df['genres'].head(3)


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
# Apply clean_data function to your features.
features = ['authors', 'genres']

for feature in features:
    books_df[feature] = books_df[feature].apply(clean_data)


def create_soup(x):
    return ' '.join(x['authors']) + ' ' +  ' '.join(x['genres'])
# Create a new soup feature
books_df['soup'] = books_df.apply(create_soup, axis=1)

# Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(books_df['soup'])


# Compute the Cosine Similarity matrix based on the count_matrix
from sklearn.metrics.pairwise import cosine_similarity

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
# Reset index of your main DataFrame and construct reverse mapping as before
books_df.head(3)
books_df = books_df.reset_index()
books_df.head(3)
indices = pd.Series(books_df.index, index=books_df['original_title'])
'''
# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]
    print('index===', idx)
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    print(sim_scores)

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return books_df['original_title'].iloc[movie_indices]


get_recommendations('Little Women', cosine_sim2)
'''


def get_recommendations_byID(id_,topN):
    # Get the index of the movie that matches the title
    #id_=25
    #topN=5
    idx = id_ - 1
    print('index===', idx)
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim2[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:topN]
    print(sim_scores)

    # Get the movie indices
    book_ids ={}
    for i in sim_scores:
        idx= i[0] +1
        if(topN >=4):
            score=1
        elif(topN>2 and topN<=3):
            score=2
        elif(topN==2):
            score=3
        else:
            score=0
        book_ids[idx]=score
    #movie_indices = [i[0] for i in sim_scores]
    print(book_ids)

    # Return the top 10 most similar movies
    return book_ids
    #books_df['original_title'].iloc[movie_indices]

'''
def get_genre_author_based_recommendation(user_responded):
    #user_responded = [490,345,195,124]	
    #['623','670','699','706','686','716','1098','2','18','21','23']	
    rec_list_per_book={}
    for ids in user_responded:
        ids=int(ids)
        list_bids = get_recommendations_byID(ids, cosine_sim2)
        rec_list_per_book[ids]=list_bids
'''    






