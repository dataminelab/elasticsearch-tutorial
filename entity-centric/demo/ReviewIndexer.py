import csv
from elasticsearch import helpers
from elasticsearch import Elasticsearch
import sys
import zipfile
import StringIO

filename = 'anonreviews.csv.zip'
es = Elasticsearch()
indexName = "anonreviews"
actionsPerBulk=5000
es.indices.delete(index=indexName, ignore=[400, 404])
indexSettings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "review": {
            "properties": {

                "reviewerId": {
                    "type": "keyword"
                },
                "vendorId": {
                    "type": "keyword"
                },
                "date": {
                    "type": "date",
                    "format" : "yyyy-MM-dd HH:mm"
                },
                "rating": {
                    "type": "integer"
                }

            }
        }
    }
}
es.indices.create(index=indexName, body=indexSettings)
actions = []

fields = []
with zipfile.ZipFile(filename) as z:
    for zippedFilename in z.namelist():
        numLines = 0
        data = StringIO.StringIO(z.read(zippedFilename))
        reader = csv.reader(data)
        for row in reader:
            numLines += 1
            if numLines == 1:
                fields = row
            else:
                doc = {
                	'reviewerId': row[0],
                 	'vendorId': row[1],
                 	'rating':int(row[2]),
                 	'date':row[3]
                }
                action = {
                        "_index": indexName,
                        '_op_type': 'index',
                        "_type": "review",
                        "_source": doc
                }
                actions.append(action)
                # Flush bulk indexing action if necessary
                if len(actions) >= actionsPerBulk:
                    try:
                        helpers.bulk(es, actions)
                    except:
                        print ("Unexpected error:", sys.exc_info()[0])
                    del actions[0:len(actions)]
                    print (numLines)

if len(actions) > 0:
    helpers.bulk(es, actions)
