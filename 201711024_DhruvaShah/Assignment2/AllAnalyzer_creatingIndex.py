import csv

from elasticsearch import Elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])

es = Elasticsearch()

INDEX_NAME = 'booklib'
with open('C:\\Users\\Foram\\Desktop\\Project\\bx-books-test-1.csv', 'r', encoding='utf-8') as csvfile:
    csv_file_object = csv.reader(csvfile, delimiter=',')
    #for row in csv_file_object:
    #    print (row)

    header = next(csv_file_object)
    header = [item.lower().replace(u'\ufeff', '') for item in header]
    print(header)
    bulk_data = [] 
    for row in csv_file_object:
        data_dict = {}
        for i in range(len(row)):
            data_dict[header[i]] = row[i]
        op_dict = {
            "index": {
                "_index": 'booklib', 
                "_type": 'Book', 
                "_id": data_dict['isbn']
            }
        }
        bulk_data.append(op_dict)
        bulk_data.append(data_dict)
    print(bulk_data)

    from elasticsearch import Elasticsearch
    # create ES client, create index
    es=Elasticsearch([{'host':'localhost','port':9200}])
    if es.indices.exists('booklib'):
        print("deleting '%s' index..." % ('booklib'))
        res = es.indices.delete(index = 'booklib')
        print(" response: '%s'" % (res))
    # since we are running locally, use one shard and no replicas
    request_body = {
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 0,
#creating the custom analyzer which will use the filter my_stop which will discard the stop words(and,is,the) just like stop analyzer and tockenize the words to lowercase just like the lowercase analyzer do
            "analysis": {
                "filter": {
                    "my_stop": {
                        "type": "stop",
                        "stopwords": ["and", "is", "the"]
                    }
                },
                "analyzer":{
                    "My_analyzer":{
                        "tokenizer":"lowercase",
                        "filter":"my_stop"
                    }
                }
            },
            },
            "mappings": {
                "Book": {
                    "properties": {
                        "book-title": {
                            "type": "text",
                            "index_options": "offsets",
    #Applying the 'simple' analyzer to the indexing of author field
    #The simple analyzer divides text into terms whenever it encounters a character which is not a letter. It lowercases all terms.
                            "analyzer":"simple",
    #Applying the 'My_analyzer' analyzer to the search_mapping on author field        
                            "search_analyzer": "My_analyzer"
                        },
                         "book-author": {
                            "type": "text",
                            "index_options": "offsets",
    #Applying the 'fingerprint' analyzer to the indexing of author field
                            "analyzer":"fingerprint",
    #Applying the 'fingerprint' analyzer to the search_mapping on author field
    #The fingerprint analyzer is a specialist analyzer which creates a fingerprint which can be used for duplicate detection.
                            "search_analyzer": "fingerprint"
                        },
                        "genre": {
                            "type": "text",
                            "index_options": "offsets",
    #Applying the 'keyword' analyzer to the indexing of author field
    #The keyword analyzer is a “noop” analyzer that accepts whatever text it is given and outputs the exact same text as a single term.
                            "analyzer":"keyword",
    #Applying the 'keyword' analyzer to the search_mapping on author field        
                            "search_analyzer": "keyword"
                        }
                    }
                }
            }
    }
    print("creating '%s' index..." % ('booklib'))
    res = es.indices.create(index = 'booklib', body = request_body)
    print(" response: '%s'" % (res))
    # bulk index the data
    print("bulk indexing...")
    res = es.bulk(index = 'booklib', body = bulk_data, refresh = True)
    res = es.search(index = INDEX_NAME,body={"query": {"match": {"book-author" : "Amy Tan"}}})
    print("results: for author")
    for hit in res['hits']['hits']:
        print(hit["_source"])
    res = es.search(index = INDEX_NAME,body={"query": {"match": {"book-title" : "The NoteBook"}}})
    print("results: for title")
    for hit in res['hits']['hits']:
        print(hit["_source"])
    res = es.search(index = INDEX_NAME,body={"query": {"match": {"genre" : "Historical"}}})
    print("results:")
    for hit in res['hits']['hits']:
        print(hit["_source"])
    #Here we have applied the 'standard' analyzer on the text so it will divides text into terms on word boundaries and  removes most punctuation, lowercases terms, and supports removing stop words. 
    res=es.indices.analyze(body={"text":"this is how the standard analyzer works","analyzer":"standard"})
    print(" response of standard analyzer: '%s'" % (res))
    #Here we have applied the 'simple' analyzer on the text so it will divide text into terms whenever it encounters a character which is not a letter. It lowercases all terms. 
    res=es.indices.analyze(body={"text":"this is how the Simple123ANALYZER works","analyzer":"simple"})
    print(" response of simple analyzer: '%s'" % (res))
    #Here we have applied the 'WHITESPACE' analyzer on the text so it will divide text into terms whenever it encounters any whitespace character. It does not lowercase terms. 
    res=es.indices.analyze(body={"text":"this is how the WHITESPACE ANALYZER works","analyzer":"whitespace"})
    print(" response of whitespace analyzer: '%s'" % (res))
    #Here we have applied the 'PATTERN' analyzer on the text so it uses a regular expression to split the text into terms. The regular expression should match the token separators not the tokens themselves. The regular expression defaults to \W+ (or all non-word characters).
    res=es.indices.analyze(body={"text":"this's how the pattern ANALYZER works,it has \W+ pattern by default","analyzer":"pattern"})
    print(" response of pattern analyzer: '%s'" % (res))

    
