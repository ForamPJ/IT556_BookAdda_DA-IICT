from elasticsearch import Elasticsearch
# create ES client, create index
es=Elasticsearch([{'host':'localhost','port':9200}])
if es.indices.exists('userlib'):
    print("deleting '%s' index..." % ('userlib'))
    res = es.indices.delete(index = 'userlib')
    print(" response: '%s'" % (res))
#changed only requestbody from mapping of Userlib
request_body = {
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        'mappings': {
            'User': {
                'properties': {
                    "text": {
                        "type": "text",
                        "index_options": "offsets"
                    },
	    "default_field": {                   #The default_field uses the BM25 similarity.
          "type": "text"
        },
        "classic_field": {                  #The classic_field uses the classic similarity (ie TF/IDF).
          "type": "text",
          "similarity": "classic" 
        },
        "boolean_sim_field": {              #The boolean_sim_field uses the boolean similarity.
          "type": "text",
          "similarity": "boolean" 
        }
	        }
            }
        }
    }
        
print("creating '%s' index..." % ('userlib'))
res = es.indices.create(index = 'userlib', body = request_body)
print(" response: '%s'" % (res))