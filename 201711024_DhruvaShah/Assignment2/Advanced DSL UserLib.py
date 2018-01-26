###########Compound Queries###################
    
    
###########Boolean Queries####################


#user id who lives in City 3, with occupation T, 
#age between [15,50] and with search-keywords Romance or Crime     

res = es.search(index = 'userlib', body={
 "query": {
    "bool" : {
      "must" : {
        "match" : { "location" : "City3" }
      },
      "filter": {
        "match" : { "occupation" : "T" }
      },
      "must_not" : {
        "range" : {
          "age" : { "gte" : 15, "lte" : 50 }
        }
      },
      "should" : [
        { "match" : { "search-keywords" : "Romance" } },
        { "match" : { "search-keywords" : "Crime" } }
      ]
    }
  }
        })
print(" response: '%s'" % (res))


#users who lives in City2

res = es.search(index = 'userlib', body={
"query": {
    "bool": {
      "filter": {
        "match": {
          "location": "City2"
        }
      }
    }
  }
        })
print(" response: '%s'" % (res))   

#All users whose occupation is Teacher
res = es.search(index = 'userlib', body={
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "match": {
          "occupation": "T"
        }
      }
    }
  }
})
print(" response: '%s'" % (res))   

#Users whose age is 30
res = es.search(index = 'userlib', body={
 "query": {
    "constant_score": {
      "filter": {
        "match": {
          "age": "30"
        }
      }
    }
  }
  })
print(" response: '%s'" % (res))  



#################Boost Queries#########################


#Here Score is changing from each query to query
#search-keywords is Romance also includes location as city1

res = es.search(index = 'userlib', body={
"query": {
        "boosting" : {
            "positive" : {
                "match" : {
                    "search-keywords" : "Romance"
                }
            },
            "negative" : {
                 "match" : {
                     "location" : "city1"
                }
            },
            "negative_boost" : 0.7
        }
    }
    })
print(" response: '%s'" % (res))  


#search-keywords is Crime also includes location as city1

res = es.search(index = 'userlib', body={
"query": {
        "boosting" : {
            "positive" : {
                "match" : {
                    "search-keywords" : "Crime"
                }
            },
            "negative" : {
                 "match" : {
                     "location" : "city1"
                }
            },
            "negative_boost" : 0.7
        }
    }
    })
print(" response: '%s'" % (res))  


#search-keywords is Romance also includes location as city3

res = es.search(index = 'userlib', body={
"query": {
        "boosting" : {
            "positive" : {
                "match" : {
                    "search-keywords" : "Romance"
                }
            },
            "negative" : {
                 "match" : {
                     "location" : "city3"
                }
            },
            "negative_boost" : 0.7
        }
    }
    })
print(" response: '%s'" % (res))  



##################Minimum Should Match Query######################



#min_should_match=2 indicates that at at least two of the conditional clauses 
#in our boolean query have to match 
#for us to consider the document a match for the query.


#min_should_match=-1 will be same as min_should_match=1 
#(since here 2 should, 2-1=1, if 3 should then 3-1=2, then same as min_should_match=2)


#User with occupation T and who live in City1 and search-keyword is either Fiction or Novel

res = es.search(index = 'userlib', body={
 "query": {
    "bool" : {
      "must" : {
        "match" : { "location" : "City1" }
      },
      "filter": {
        "match" : { "occupation" : "S" }
      },
      "should" : [
        { "match" : { "search-keywords" : "Fiction" } },
        { "match" : { "search-keywords" : "Novel" } }
      ],
       "minimum_should_match" : 1,
    }
    }
   })
print(" response: '%s'" % (res))

#user with occupation S and search-keyword Romance and location city3

res = es.search(index = 'userlib', body={
 "query": {
    "bool" : {
      "must" : {
        "match" : { "occupation" : "S" }
      },
      "should" : [
        { "match" : { "search-keywords" : "Romance" } },
        { "match" : { "location" : "city3" } }
      ],
       "minimum_should_match" : 2,
    }
    }
   })
print(" response: '%s'" % (res))


#user with occupation S 

res = es.search(index = 'userlib', body={
 "query": {
    "bool" : {
      "must" : {
        "match" : { "occupation" : "S" }
      },
      "should" : [
        { "match" : { "search-keywords" : "Romance" } },
        { "match" : { "location" : "city3" } }
      ],
       "minimum_should_match" : 0,
    }
    }
   })
print(" response: '%s'" % (res))


#user with occupation S and search-keyword Romance or location city3

res = es.search(index = 'userlib', body={
 "query": {
    "bool" : {
      "must" : {
        "match" : { "occupation" : "S" }
      },
      "should" : [
        { "match" : { "search-keywords" : "Romance" } },
        { "match" : { "location" : "city3" } }
      ],
       "minimum_should_match" : -1,
    }
    }
   })
print(" response: '%s'" % (res))
