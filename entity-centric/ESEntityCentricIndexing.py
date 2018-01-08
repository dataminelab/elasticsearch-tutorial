from elasticsearch import helpers
from elasticsearch.client import Elasticsearch
import time
import argparse
import json

#   This is a generic script to scroll information from one event-centric index sorted 
#   by entity ID (e.g. a person) and bundle related events in update calls to an entity
#   centric index which summarises behaviours over time 

parser = argparse.ArgumentParser()
parser.add_argument("eventIndexName", help="The name of the index which will receive events")
parser.add_argument("eventDocType", help="Name of the event type")
parser.add_argument("eventQueryFile", help="The JSON file with the query for events")
parser.add_argument("entityIdField", help="The name of the field with the entity ID")
parser.add_argument("entityIndexName", help="The name of the index which will build entities")
parser.add_argument("entityDocType", help="Name of the entity type")
parser.add_argument("updateScriptFile", help="The script file used to update entities with events")

parser.add_argument("-actionsPerBulk", help="The number of records to send in each bulk request", type=int, default=5000)
parser.add_argument("-eventsPerScrollPage", help="The number of events per scroll page (small=slow)",  type=int, default=5000)
parser.add_argument("-maxTimeToProcessScrollPage", help="The max time to process page of events",  default="1m")
parser.add_argument("-scriptMode", help="The mode parameter passed to the script", default="fullBuild")
args = parser.parse_args()

eventsQuery = json.load(open(args.eventQueryFile))
es = Elasticsearch()

def generate_actions():
    def get_action(events):
        return {
            '_op_type': 'update',
            "_id": lastEntityId,
            "scripted_upsert":True,
            "script": {
                "file": args.updateScriptFile,
                        "params": {
                            "scriptMode": args.scriptMode,
                            "events":list(events)
                        }
            },            
            "upsert" : {
            # Use a blank document because script does all the initialization
            }
        }

    lastEntityId = ""
    events = []
    numDocsProcessed = 0
    start = time.time()
    for doc in helpers.scan(es,
            index=args.eventIndexName,
            doc_type=args.eventDocType,
            query=eventsQuery,
            size=args.eventsPerScrollPage,
            scroll=args.maxTimeToProcessScrollPage,
            preserve_order=True):

        thisEntityId = doc["_source"][args.entityIdField]

        # end of event group
        if thisEntityId != lastEntityId:
            if events:
                yield get_action(events)
            events = []
            lastEntityId = thisEntityId
        events.append(doc["_source"])
        numDocsProcessed += 1
        if numDocsProcessed % 10000 == 0:
            elapsedSecs = int(time.time() - start)
            dps =  numDocsProcessed/max(1,elapsedSecs)
            print numDocsProcessed, "docs per second=",dps

    # load last event group too
    if events:
        yield get_action(events)

    print "Processed", numDocsProcessed, "docs"

start = time.time()
helpers.bulk(es, generate_actions(),
    index=args.entityIndexName,
    doc_type=args.entityDocType,
    chunk_size=args.actionsPerBulk)

elapsed = (time.time() - start)
print "elapsed time=",elapsed
