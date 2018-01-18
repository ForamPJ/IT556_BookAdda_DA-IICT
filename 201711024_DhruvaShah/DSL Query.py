
#query for all displaying all records of dataset
    res = es.search(index = 'userlib', body={"query": {"match_all": {}}})
    print(" response: '%s'" % (res))
    
    res = es.search(index = 'booklib', body={"query": {"match_all": {}}})
    print(" response: '%s'" % (res))
    
    
#query for displaying users with location as City2        
    res = es.search(index = 'userlib', body={
   "query":{
      "match" : {
         "location":"City2"
      }
   }
})
    print(" response: '%s'" % (res))
    
    
#query for displaying book that contain with string as Buttermilk Sky
    res = es.search(index = 'booklib', body={
   "query":{
       "query_string":{
         "query":"Buttermilk Sky"
      }
   }
   }
)
    print(" response: '%s'" % (res))
    
#query for displaying books with YOP as 1999

    res = es.search(index = 'booklib', body={
   "query":{
      "term":{"year-of-publication":"1999"}
   }
   }
)
    print(" response: '%s'" % (res))

#query for displaying  user age greater than equal to 20

    res = es.search(index = 'userlib', body={
   "query":{"range":{
         "age":{
            "gte":20
         }
      }
      
   }
   }
)
    print(" response: '%s'" % (res))
    
    
    
    
    
#query for displaying datapoints on the basis of type value

    res = es.search(index = 'booklib', body={
   "query":{
      
      "type" : {
         "value" : "Book"
      }
   }
   }
 
)
    print(" response: '%s'" % (res))
    
    #query for displaying location as city3 where searched keyword crime

    res = es.search(index = 'userlib', body={
            
           "query": {
                   "bool": {
                           "must": [
                                   { "match": { "location": "City3" } }
                                   ],
                                   "must_not": [
                                    { "match": { "search-keywords": "Crime" } }
      ]
    }
  }
   }
)
    print(" response: '%s'" % (res))

#query for displaying datapoints with location as city3 and search-keyword as crime

    res = es.search(index = 'userlib', body={
                
               "query": {
                       "bool": {
                               "must": [
                                       { "match": { "location": "City3" } },
                                       {  "match": { "search-keywords": "Crime" } }
                                       ]
                               }
                       }
                                           }
    )
    print(" response: '%s'" % (res))
    
#query for displaying datapoints with location as city3 or search-keyword as crime
    res = es.search(index = 'userlib', body={
                
               "query": {
                       "bool": {
                               "should": [
                                       { "match": { "location": "City3" } },
                                       {  "match": { "search-keywords": "Crime" } }
                                       ]
                               }
                       }
                                           }
    )
    print(" response: '%s'" % (res))
