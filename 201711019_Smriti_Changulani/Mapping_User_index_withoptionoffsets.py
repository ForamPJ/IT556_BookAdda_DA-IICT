import csv

from elasticsearch import Elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])

es = Elasticsearch()


with open('C:\\Users\\Foram\\Desktop\\Project\\bx-user-test-1.csv', 'r', encoding='utf-8') as csvfile:
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
                "_index": 'userlib', 
                "_type": 'User', 
                "_id": data_dict['user-id']
            }
        }
        bulk_data.append(op_dict)
        bulk_data.append(data_dict)
    print(bulk_data)

    from elasticsearch import Elasticsearch
    # create ES client, create index
    es=Elasticsearch([{'host':'localhost','port':9200}])
    if es.indices.exists('userlib'):
        print("deleting '%s' index..." % ('userlib'))
        res = es.indices.delete(index = 'userlib')
        print(" response: '%s'" % (res))
    # since we are running locally, use one shard and no replicas
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
                    }
	        }
            }
        }
    }
    print("creating '%s' index..." % ('userlib'))
    res = es.indices.create(index = 'userlib', body = request_body)
    print(" response: '%s'" % (res))
    # bulk index the data
    print("bulk indexing...")
    res = es.bulk(index = 'userlib', body = bulk_data, refresh = True)
    
