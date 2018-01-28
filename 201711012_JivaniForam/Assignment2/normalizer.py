
ES_HOST = {"host" : "localhost" , "port" : 9200}
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts = [ES_HOST])
if es.indices.exists('booklib'):
    print("deleting '%s' index..." % ('booklib'))
    res = es.indices.delete(index = 'booklib')
    print(" response: '%s'" % (res))


request_body = {
	'PUT':{
		"settings": {
		"number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
        	"normalizer":{
        		"book_normalizer":{
        			"type":"custom",
        			"char_filter":[],
        			"filter":["lowercase" , "asciifolding"]
        		}
        	}

       	 },
       	 "mappings":{
       	 	"type":{
       	 		"properties": {
       	 			"text":{
       	 				"type": "text",
       	 				"normalizer" : "book_normalizer"
       	 			}
       	 		}
       	 	}
       	 }
		}
	}
}

print("creating '%s' index..." % ('booklib'))
res = es.index(index = 'booklib',doc_type='post', body = request_body)
print(" response: '%s'" % (res))

import csv

from elasticsearch import Elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])

es = Elasticsearch()


with open('C:\\Users\\admin\\Desktop\\Project\\bx-books-test-1.csv', 'r', encoding='utf-8') as csvfile:
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
