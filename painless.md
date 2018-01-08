## Painless

Test data set:
```
PUT hockey/player/_bulk?refresh
{"index":{"_id":1}}
{"first":"johnny","last":"gaudreau","goals":[9,27,1],"assists":[17,46,0],"gp":[26,82,1],"born":"1993/08/13"}
{"index":{"_id":2}}
{"first":"sean","last":"monohan","goals":[7,54,26],"assists":[11,26,13],"gp":[26,82,82],"born":"1994/10/12"}
{"index":{"_id":3}}
{"first":"jiri","last":"hudler","goals":[5,34,36],"assists":[11,62,42],"gp":[24,80,79],"born":"1984/01/04"}
{"index":{"_id":4}}
{"first":"micheal","last":"frolik","goals":[4,6,15],"assists":[8,23,15],"gp":[26,82,82],"born":"1988/02/17"}
{"index":{"_id":5}}
{"first":"sam","last":"bennett","goals":[5,0,0],"assists":[8,1,0],"gp":[26,1,0],"born":"1996/06/20"}
{"index":{"_id":6}}
{"first":"dennis","last":"wideman","goals":[0,26,15],"assists":[11,30,24],"gp":[26,81,82],"born":"1983/03/20"}
{"index":{"_id":7}}
{"first":"david","last":"jones","goals":[7,19,5],"assists":[3,17,4],"gp":[26,45,34],"born":"1984/08/10"}
{"index":{"_id":8}}
{"first":"tj","last":"brodie","goals":[2,14,7],"assists":[8,42,30],"gp":[26,82,82],"born":"1990/06/07"}
{"index":{"_id":39}}
{"first":"mark","last":"giordano","goals":[6,30,15],"assists":[3,30,24],"gp":[26,60,63],"born":"1983/10/03"}
{"index":{"_id":10}}
{"first":"mikael","last":"backlund","goals":[3,15,13],"assists":[6,24,18],"gp":[26,82,82],"born":"1989/03/17"}
{"index":{"_id":11}}
{"first":"joe","last":"colborne","goals":[3,18,13],"assists":[6,20,24],"gp":[26,67,82],"born":"1990/01/30"}
```

Calculate the score using script:

```
GET hockey/_search
{
  "query": {
    "function_score": {
      "script_score": {
        "script": {
          "source": "int total = 0; for (int i = 0; i < doc['goals'].length; ++i) { total += doc['goals'][i]; } return total;"
        }
      }
    }
  }
}
```

Create scripted field:
```
GET hockey/_search
{
  "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_goals": {
      "script": {
        "lang": "painless",
        "source": "int total = 0; for (int i = 0; i < doc['goals'].length; ++i) { total += doc['goals'][i]; } return total;"
      }
    }
  }
}
```

Sort players by the first/last name:

```
GET hockey/_search
{
  "query": {
    "match_all": {}
  },
  "sort": {
    "_script": {
      "type": "string",
      "order": "asc",
      "script": {
        "lang": "painless",
        "source": "doc['first.keyword'].value + ' ' + doc['last.keyword'].value"
      }
    }
  }
}
```

Update fields with Painless:
```
POST hockey/player/1/_update
{
  "script": {
    "lang": "painless",
    "source": "ctx._source.last = params.last",
    "params": {
      "last": "hockey"
    }
  }
}
```

Update document and add fields:
```
POST hockey/player/1/_update
{
  "script": {
    "lang": "painless",
    "source": "ctx._source.last = params.last; ctx._source.nick = params.nick",
    "params": {
      "last": "gaudreau",
      "nick": "hockey"
    }
  }
}
```

Debugging:

```
PUT /hockey/player/1?refresh
{"first":"johnny","last":"gaudreau","goals":[9,27,1],"assists":[17,46,0],"gp":[26,82,1]}

POST /hockey/player/1/_explain
{
  "query": {
    "script": {
      "script": "Debug.explain(doc.goals)"
    }
  }
}

POST /hockey/player/1/_update
{
  "script": "Debug.explain(ctx._source)"
}
```


## Filter with the Painless script

Test data set
```
PUT /tweets/tweet/_bulk?refresh
{"index":{"_id":1}}
{"username":"tom","posted_date":"2017/07/25" ,"message": "I brought apple stock at the best price" ,"tags": ["stock","money"] , "info":{"device":"mobile", "os": "ios"}, "likes": 10}
{"index":{"_id":2}}
{"username":"mary","posted_date":"2017/06/25" ,"message": "Machine learning is the future" ,"tags": ["ai","tech"] , "info":{"device":"desktop", "os": "ios"}, "likes": 100}
{"index":{"_id":3}}
{"username":"tom","posted_date":"2017/07/27" ,"message": "just tweeting" ,"tags": ["confused"] , "info":{"device":"mobile", "os": "win"}, "likes": 0}
{"index":{"_id":4}}
{"username":"mary","posted_date":"2017/07/28" ,"message": "exploring painless" ,"tags": ["elastic"] , "info":{"device":"mobile", "os": "linux"}, "likes": 100}
{"index":{"_id":5}}
{"username":"mary","posted_date":"2017/05/20" ,"message": "painless is fun but its a new scripting language in the town" ,"tags": ["elastic","painless","scripting"] , "info":{"device":"mobile", "os": "linux"}, "likes": 1000}
```

## Script Query

Embed the script in a script object (`“script” :{}`)

```
POST /tweets/tweet/_search
{  
  "query":{  
     "bool":{  
        "must":[  
           {  
              "match":{  
                 "message":"painless"
              }
           }
        ],
        "filter":[  
           {  
              "script":{  
                 "script":{  
                    "source":"doc['message.keyword'].value.length() > params.length",
                    "params":{  
                       "length":25
                    }
                 }
              }
           }
        ]
     }
  }
}
```

## Aggregations

Find number of tweets per month

```
POST /tweets/tweet/_search
{  
  "size":0,
  "aggs":{  
     "my_terms_agg":{  
        "terms": {  
           "script":{  
              "source":"doc['posted_date'].date.monthOfYear"
           }
        }
     }
  }
}
```


## Deleting a Field Using Scripts
```
POST /tweets/tweet/5/_update
{  
  "script":{  
     "source":"ctx._source.info.remove(params.fieldname)",
     "params":{  
        "fieldname": "device"
     }
  }
}
```


## Custom scoring

Instead of using TF/IDF we create a custom scoring algorithm.
Other scenarios:
* Sorting by most popular/read articles
* Sorting items by custom user logic
* Sorting items by revenue

```
POST /tweets/tweet/_search
 {
   "query": {
       "function_score": {
           "query": {
               "match": { "message": "painless" }
           },
           "script_score" : {
               "script" : {
                 "source": "Math.log(1 + doc['likes'].value)"
               }
           }
       }
   }
}
```


Based on:
https://qbox.io/blog/advanced-methods-for-painless-scripting-with-elasticsearch-part-2
https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-examples.html

See also:
https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-debugging.html