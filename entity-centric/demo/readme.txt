Entity centric demo
===================

Background
===========
This demo accompanies the "Entity-centric indexing" talk from Elastic{on} 2015 and
uses some anonymized real-world data to build profiles of buyer behaviours based
on their behaviour in the Amazon marketplace.
The talk provides useful background and a recording is here: https://www.elastic.co/videos/entity-centric-indexing-mark-harwood

UPDATE - 17th March 2017
This version has been adapted to use the new Painless scripting language and has been 
tested with elasticsearch version 5.2.2

Loading the data, building entities
====================================
1) Run the script "loadEvent.sh". This will drop then create the "anonreviews" index
2) Install the "ReviewerProfileUpdater.painless" file in the $ES_HOME/config/scripts directory
3) Run the script "buildEntities.sh" to pull the reviews sorted by reviewerId and time from
the "anonreviews" index and it will create "reviewer" documents in a "reviewers" index.

Step 3 relies on 2 scripts 
1) ESEntityCentricIndexing.py - generic script to pull data from
an event-centric index and push to an entity-centric one.
2) ReviewerProfileUpdater.painless - our domain-specific business logic for summarising reviewer behaviour

Interesting query
===================
//Find the seller who has more than their fair-share of "fanboy" reviewers..
```
GET reviewers/_search
{
    "query": {
        "match": {
            "profile": "fanboy"
        }
    },
    "aggs": {
        "keywords": {
            "significant_terms": {
                "field": "vendors.vendorId"
            }
        }
    }
}
```