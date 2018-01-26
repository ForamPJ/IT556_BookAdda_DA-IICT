###########COMPOUND QUERIES#########

#1.#########BOOLEAN FORMATION##########

#query to display book data with genre as hitorical with book author as robert cowley 
#with year of publication not between 2004 & 2017 ...with no of pages as 400 or 251

    res = es.search(index = 'booklib', body={
            "query": {
                    
                        "bool" : {
                          "must" : {
                            "match" : { "genre" : "Historical" }
                          },
                          "filter": {
                            "match" : { "book-author" : "Robert Cowley" }
                          },
                          "must_not" : {
                            "range" : {
                              "year-of-publication" : { "gte" : 2004, "lte" : 2017 }
                            }
                          },
                          "should" : [
                            { "match" : { "sizeofpages" : 400 } },
                            { "match" : { "sizeofpages" : 251 } }
                          ]
                          
                        }
                      }
                    })
    print(" response: '%s'" % (res))


#display datapoint with book author as john grisham

    res = es.search(index = 'booklib', body={
            "query": {
                    "bool": {
                              "filter": {
                                "match": {
                                  "book-author": "John Grisham"
                                }
                              }
                            }
                        
                      }
                    })
    print(" response: '%s'" % (res))
    
#display all datapoints with genre g1

    res = es.search(index = 'booklib', body={
            "query": {
                    "bool": {
                              "must": {
                                "match_all": {}
                              },
                              "filter": {
                                "term": {
                                  "genre": "g1"
                                }
                              }
                            }
                        
                      }
                    })
    print(" response: '%s'" % (res))

#2.##########BOOSTING############

#boosting query for booklib   

    res = es.search(index = 'booklib', body={
            "query": {
                        "boosting" : {
                                    "positive" : {
                                        "term" : {
                                            "year-of-publication" : "2000"
                                        }
                                    },
                                    "negative" : {
                                         "term" : {
                                             "genre" : "g1"
                                        }
                                    },
                                    "negative_boost" : 0.6
                                }
                        
                      }
                    })
    print(" response: '%s'" % (res))
    
#YOP changed to 1999

        res = es.search(index = 'booklib', body={
            "query": {
                        "boosting" : {
                                    "positive" : {
                                        "term" : {
                                            "year-of-publication" : "1999"
                                        }
                                    },
                                    "negative" : {
                                         "term" : {
                                             "genre" : "g1"
                                        }
                                    },
                                    "negative_boost" : 0.6
                                }
                        
                      }
                    })
    print(" response: '%s'" % (res))
    
#genre changed to historical

        res = es.search(index = 'booklib', body={
            "query": {
                        "boosting" : {
                                    "positive" : {
                                        "term" : {
                                            "year-of-publication" : "1999"
                                        }
                                    },
                                    "negative" : {
                                         "term" : {
                                             "genre" : "Historical"
                                        }
                                    },
                                    "negative_boost" : 0.6
                                }
                        
                      }
                    })
    print(" response: '%s'" % (res))
    
    
############MINIMUM_SHOULD_MATCH QUERIES#############

#query to display with minimum_should_match as 1 (or-2) will give datapoints with 
#sizeofpage as 600 or genre as g1 or YOP as 1999

    res = es.search(index = 'booklib', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "sizeofpages" : 600 } },
                            { "match" : { "genre" : "g1" } },
                            { "match" : { "year-of-publication" : 1999 } }
                          ],
                              "minimum_should_match" : 1
                          
                        }
                      }
                    })
    print(" response: '%s'" % (res))
    
    
#query to display with minimum_should_match as 2 (or-1) will give datapoints with 
#combination of any of these two (sizeofpage as 600 or genre as g1 or YOP as 1999)

    res = es.search(index = 'booklib', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "sizeofpages" : 600 } },
                            { "match" : { "genre" : "g1" } },
                            { "match" : { "year-of-publication" : 1999 } }
                          ],
                              "minimum_should_match" : -1
                          
                        }
                      }
                    })
    print(" response: '%s'" % (res))
    
    
#query to display with minimum_should_match as 3  will give datapoints with 
#sizeofpage as 600 and genre as g1 and YOP as 1999

    res = es.search(index = 'booklib', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "sizeofpages" : 600 } },
                            { "match" : { "genre" : "g1" } },
                            { "match" : { "year-of-publication" : 1999 } }
                          ],
                              "minimum_should_match" : 3
                          
                        }
                      }
                    })
    print(" response: '%s'" % (res))
    

    
#query to display with minimum_should_match as 4 will give 0 records as only 3 should_match 
#clauses are there

    res = es.search(index = 'booklib', body={
            "query": {
                    
                        "bool" : {
                          
                          "should" : [
                            { "match" : { "sizeofpages" : 600 } },
                            { "match" : { "genre" : "g1" } },
                            { "match" : { "year-of-publication" : 1999 } }
                          ],
                              "minimum_should_match" : 4
                          
                        }
                      }
                    })
    print(" response: '%s'" % (res))
