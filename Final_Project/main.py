# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 13:59:31 2018

@author: Foram
"""
import load_data as ld
import svd as SVD_train_test
import pandas as pd
from prettytable import PrettyTable

import IISIM_final as IISIM
import genre_author_based as GenAuthBased
import get_similarbooks_by_author as SIM_Auth

# steps 

def get_new_recoomendation(rated_liked_items):
    #rated_liked_items = {372:5,89:4,709:2,562:1,189:0,157:0}
    #rated_liked_items= {27: 2, 67: 1, 325: 0, 372: 4, 562: 0, 862: 5,89:4}
    rated_item_list=[]
    topN=1
    #top_n_GenAuthSIM_idx =[]
    #rec_list_GenAuthSIM={}
    for item in rated_liked_items:
        rated_item_list.append(item)
        given_rating = rated_liked_items[item]
        if(given_rating>0):
            if(given_rating >3):
                topN= given_rating - 1
            elif(given_rating>1 and given_rating<=3):
                topN=2
            else:
                topN=1
            top_n_IISIM =IISIM.get_similar_books( item ,topN)
            print(top_n_IISIM)
            #rec_list_IISIM[item]=top_n_IISIM
            print(topN)
            top_n_GenAuthSIM = GenAuthBased.get_recommendations_byID(item,topN)
            #top_n_GenAuthSIM_idx.extend(top_n_GenAuthSIM.index+1)
            print(top_n_GenAuthSIM)
            #rec_list_GenAuthSIM[ids]=top_n_GenAuthSIM
            
    
    
    
    user_responded =list(k for k, v in rated_liked_items.items() if v != 0)
    
    #user_responded_ratings =list(v for k, v in rated_liked_items.items() if v != 0)
    list_ids_SIM_Auth = SIM_Auth.get_similar_by_author(user_responded)
    
    new_rec_list=[]
    new_dic={}
    #new_lis =[]
    for ids in top_n_IISIM:
        dic= top_n_IISIM[ids]
        for di in dic:
            new_dic[di]=dic[di]
        print(new_dic)
    
    for ids in top_n_GenAuthSIM:
        if not (ids in new_dic):
            new_dic[ids]=top_n_GenAuthSIM[ids]
        print(new_dic)
    
    list_with_1sthigh =[k for k,v in new_dic.items() if v == 1]
    list_with_2ndhigh =[k for k,v in new_dic.items() if v == 2]
    list_with_3rdhigh =[k for k,v in new_dic.items() if v == 3]
    
    list_rec = list_with_1sthigh + list_with_2ndhigh + list_with_3rdhigh
    
    list_rec_= list_rec[0:8]
    new_rec_list = list_rec_
    count=1
    if (list_ids_SIM_Auth):
        for ids in list_ids_SIM_Auth:
            if not(ids in new_rec_list) and count != 3:
                new_rec_list.append(ids)
                count+=1
    else:
        new_rec_list = list_rec[0:10]
    #new_rec_list.extend(top_n_IISIM[ids])
    #new_rec_list.extend(top_n_GenAuthSIM_idx)
    #new_rec_list.extend(list_ids_SIM_Auth)
    #new_rec_list_final = list(set(new_rec_list)-set(rated_item_list))
    
    print(new_rec_list)
    
    new_rec_list = list(set(new_rec_list)-set(user_responded))
    
    print ('*User browsed books:')
    #n=1
    t = PrettyTable(['Book Id', 'Title' ])
    for ids in user_responded:
        ids =int(ids)
        row =[]
        row.append(ids)
        row.append(GenAuthBased.get_title(books[ids]))
        #row.append(GenAuthBased.get_author(books[ids]))
        #row.append(GenAuthBased.get_genres(books[ids]))
        t.add_row(row)
        #for test purpose only: comment out
        #print ids, get_title(books[ids])
        #loc = get_genres(books[ids])+get_sub_genres(books[ids])
        #print( '{0}. {1}. by [{2}]. ({3})'.format(n,GenAuthBased.get_title(books[ids]),GenAuthBased.get_author(books[ids]),GenAuthBased.get_genres(books[ids])))
        #print(get_title(books[ids]))
        #print(loc)
        #n=n+1
    print(t)    
    print('*Recommended books: ')
    #n=1
    #for idx in user_responded:
    #    idx =int(idx)
    #    list_books_per= rec_list_per_book[idx]
    t = PrettyTable(['Book Id', 'Title' ])
    for ids in new_rec_list:
        #ids = int(ids)
        #ids= ids+ 1
        id_ =ids 
        #list_books_per[list_books_per == ids].index[0]
        #id_=id_+1
        row =[]
        row.append(id_)
        row.append(GenAuthBased.get_title(books[ids]))
        #row.append(GenAuthBased.get_author(books[ids]))
        #row.append(GenAuthBased.get_genres(books[ids]))
        t.add_row(row)
        #print(id_)
                #for test purpose only: comment out
                #print '{0}. {1}, {2}'.format(n, get_title(books[ids]), ids)
                #loc = get_genres(books[ids])+get_sub_genres(books[ids])
        #print( '{0}. book ID = {1} {2}. by [{3}]. {4}'.format(n,ids,GenAuthBased.get_title(books[id_]),GenAuthBased.get_author(books[id_]),GenAuthBased.get_genres(books[id_])))
                #print( '{0}. {1}. {2}'.format(n, get_title(books[ids]),loc))
        #n+=1


    print(t)    

# step 1
just_loggedin=0
print("***********************************************************")
print("***********************************************************")
print("\nChoose Any ONE Option : \n\n1 for Login \n\n2 to Register\n")
print("***********************************************************")
print("***********************************************************")
opt_log_reg=int(input("\nEnter Option Here : "))
#print("\nOption choosed is : ",inputoption1)
useridx=0
if(opt_log_reg==1):
    print("###########################################################")
    input_userid=int(input("\nEnter Your USER-ID Here : "))
    print("\nValidating USER-ID .... ")
    df_rating, df_book, books =ld.load_data()
    just_loggedin=1
    #uuid=df_rating['user_id'].drop_duplicates()
    print("##########################################################")
elif(opt_log_reg==2):
    #functionregister()
    print('')
else:
    print("Choose a VALID OPTION !!")


def popularity_based():
    print("###########################################################")
    print("\n\n Popularity Based Recommendation (global rating)\n\n")
    print("###########################################################")
    ratemat=df_book.sort_values(by=['average_rating','ratings_count'], ascending=False)
    topxpopu=ratemat[0:5]
    t = PrettyTable(['Book Id', 'Title' , 'Rating'])
    row=[]
    row.append(topxpopu.book_id)
    row.append(topxpopu.original_title)
    row.append(topxpopu.average_rating)
    t.add_row(row)
    print(t)
    

rated_items={} 

def choose_useraction():
    #opt_continue=1
    opt_action=1
    while(opt_action==1 or opt_action==2 or opt_action==3):
        print("###########################################################")
        print("\nChoose any ONE of the following : \n\n1 for Rating\n\n2 to Like(5) dislike(0)\n\n3 for View\n\n5 or Press any other NUMERIC key to EXIT")   
        opt_action=int(input("\nEnter Your Action Option Here : "))
       
        if(opt_action==1):
            bid_opt_rating=int(input("\nFor BOOK?? (Book-ID) : "))
            print("###########################################################")
            print("\nEnter rating for book "+str(bid_opt_rating)+" : ")
            rating=(input())
            rated_items[bid_opt_rating]=int(rating)
        #functionrating(userx,inputoption7) #userID and BookID as parameters
        elif(opt_action==2):
            bid_opt_likedislike=int(input("\nFor BOOK?? (Book-ID) : "))
            rating=(input())
            rated_items[bid_opt_likedislike]=int(rating)
        #functionlike(userx,inputoption7)
        elif(opt_action==3):
            bid_opt_view=int(input("\nFor BOOK?? (Book-ID) : "))
        
        #functionview(userx,inputoption7)
        #elif(opt_action==4):
        #    book_recommendation(userx)
        else:
            break
        
#load data frames for operation
#global df_rating
#global df_book
#global df_books
# show item based on SVD when log into system
userid = input_userid
opt_get_logout =1
while(opt_get_logout == 1):
    if(just_loggedin == 1):
        
        top_n =SVD_train_test.train_test_svd(userid,df_rating,df_book)
        
        
        # Print the recommended items for each user
        t = PrettyTable(['Book Id', 'Title' , 'Rating'])
            
        for uid, user_ratings in top_n.items():
            uid = int(uid)
            if(uid==userid):
                print(uid)
                for (iid, est) in user_ratings:
                    row =[]
                    book_detail= df_book[df_book.id == iid]
                    row.append(iid)
                    row.append(book_detail['title'].values[0])
                    row.append(int(est))
                    t.add_row(row)
                    #print('book id : {0} Title : {1} Rating : {2}'.format(iid, book_detail['title'].values[0] ,est))
                        
        print(t)
        print("###########################################################")
        popularity_based()
        print("###########################################################")
        just_loggedin=0
        choose_useraction()
        print(rated_items)
        if(len(rated_items)!=0):
            get_new_recoomendation(rated_items)
        print("###########################################################")
        print("\n1 to get more recommendations \n\n2 Press any other NUMERIC key to EXIT")   
        opt_get_logout=int(input("\nEnter Here (to get more or logout) : "))
        
    else:
    ###########take input from user - ratings, like/dislike, click/view#########
    # rated Items: 1338 : 4 1198: 2 1380 : 1
    #liked item(rating as 5): 490 : 5 
    #disliked items{ratinf as 0}:862 :0 1010:0 
    #not viewd : 1488 1466 1597 1478 
    ###########################################################################
        choose_useraction()
        print(rated_items)
        get_new_recoomendation(rated_items)
        print("###########################################################")
        print("\n1 to get more recommendations \n\n2 Press any other NUMERIC key to EXIT")   
        opt_get_logout=int(input("\nEnter Here (to get more or logout) : "))
        


import csv   
#fields=[5,67,4]
with open(r'F:/Mtech/Rec Project/Kagel Dataset/ratings_test_900.csv', 'a') as f:
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    for ids in rated_items:
        fields=[]
        fields.append(userid)
        fields.append(ids)
        fields.append(rated_items[ids])
        writer.writerow(fields)
    #(df_book_IISM, book_sim_df) = IISIM.get_book_by_IISIM(df_rating,df_book)
    

    #print("\n\n1 for continue rating and likeing\n\nPress any other NUMERIC key to EXIT") 
    #opt_continue=int(input("\nEnter Your Action Option Here : "))  
#choose_useraction()
#get_new_recoomendation(rated_items)
'''

data=[]
# loop for all rated/liked/disliked books
data_per_book=[]
user_id=userid
book_id=
rating=
timestamp=
data_per_book.append([user_id,book_id,rating,timestamp])

#data.append(data_per_book)

df= pd.DataFrame()

d = {'col1': [1, 2], 'col2': [3, 4]}

df_rating_like =pd.DataFrame(rated_liked_items)

user_responded = ['623','670','699','706','686','716','1098','2','18','21','23']	
list_ids = SIM_Auth.get_similar_by_author(user_responded)
print(list_ids)
# get input raing like dislike click from user
user_input_reward= ['25','1419','488']
user_input_penlty= ['25','1419','488']
user_responded.extend(user_input_reward)
list_ids =  SIM_Auth.get_similar_by_author(user_responded)    
print(list_ids)



[27, 24, 422, 1065, 399, 168, 739, 691, 302, 107, 169, 972]
'''
