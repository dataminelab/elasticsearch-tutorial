
## Simulate the pipeline

```
POST /_ingest/pipeline/_simulate?verbose&pretty
{
  "pipeline": {
    "description": "Add user/job fields",
    "processors": [
      {
        "set": {
          "field": "user",
          "value": "john"
        }
      },
      {
        "set": {
          "field": "job",
          "value": 10
        }
      }
    ],
    "version": 1
  },
  "docs": [
    {
      "_index": "index",
      "_type": "type",
      "_id": "1",
      "_source": {
        "name": "docs1"
      }
    },
    {
      "_index": "index",
      "_type": "type",
      "_id": "2",
      "_source": {
        "name": "docs2"
      }
    }
  ]
}

```

## Built-in processors

```
POST /_ingest/pipeline/_simulate?pretty
{
  "pipeline": {
    "description": "Testing some build-processors",
    "processors": [
      {
        "dot_expander": {
          "field": "extfield.innerfield"
        }
      },
      {
        "remove": {
          "field": "unwanted"
        }
      },
      {
        "trim": {
          "field": "message"
        }
      },
      {
        "set": {
          "field": "tokens",
          "value": "{{message}}"
        }
      },
      {
        "split": {
          "field": "tokens",
          "separator": "\\s+"
        }
      },
      {
        "sort": {
          "field": "tokens",
          "order": "desc"
        }
      },
      {
        "convert": {
          "field": "mynumbertext",
          "target_field": "mynumber",
          "type": "integer"
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_type": "type",
      "_id": "1",
      "_source": {
        "extfield.innerfield": "booo",
        "unwanted": 32243,
        "message": "   155.2.124.3 GET /index.html 15442 0.038   ",
        "mynumbertext": "3123"
      }
    }
  ]
}
```

## Grok processor

```
POST /_ingest/pipeline/_simulate?pretty
{
  "pipeline": {
  "description" : "custom grok pattern",
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["my favorite color is %{COLOR:color}"],
        "pattern_definitions" : {
          "COLOR" : "RED|GREEN|BLUE"
        }
      }
    }
  ]
},
"docs":[
  {
    "_source": {
      "message": "my favorite color is RED"
    }
  },
  {
    "_source": {
      "message": "happy fail!!"
    }
  }
  ]
}
```


# Tutorial

Import sample CSV data. See:
https://data.ny.gov/Transportation/NYC-Transit-Subway-Entrance-And-Exit-Data/i9wp-a4ja/data

## Simulate pipeline

```
# Start from docs, fill in processors later
POST _ingest/pipeline/_simulate
{
 "pipeline": {},
 "docs": [
   {
     "station": "BMT,4 Avenue,59th St,40.641362,-74.017881,N,R,,,,,,,,,,Stair,YES,,YES,NONE,,FALSE,,TRUE,4th Ave,60th St,SW,40.640682,-74.018857,'(40.641362, -74.017881)','(40.640682, -74.018857)'"
   }
 ]
}
```

Simulate the grok processor:

```
POST _ingest/pipeline/_simulate
{
 "pipeline": {
   "description": "Parsing the NYC stations",
   "processors": [
     {
       "grok": {
         "field": "station",
         "patterns": [
           "%{WORD:division},%{DATA:line},%{DATA:station_name},%{NUMBER:location.lat},%{NUMBER:location.lon},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA:entrance_type},%{DATA:entry},%{DATA:exit_only},%{DATA:vending}"
         ]
       }
     },
     {
       "remove": {
         "field": "station"
       }
     }
   ]
 },
 "docs": [
   {
     "_index": "subway_info",
     "_type": "station",
     "_id": "AVvJZVQEBr2flFKzrrkr",
     "_score": 1,
     "_source": {
       "station": "BMT,4 Avenue,53rd St,40.645069,-74.014034,R,,,,,,,,,,,Stair,NO,Yes,NO,NONE,,FALSE,,TRUE,4th Ave,52nd St,NW,40.645619,-74.013688,'(40.645069, -74.014034)','(40.645619, -74.013688)'"
     }
   }
 ]
}
```

Create template for the index. It will be automatically applied when new indices are created.

```
PUT _template/nyc_template
{
 "template": "subway_info*",
 "settings": {
   "number_of_shards": 1
 },
 "mappings": {
   "station": {
     "properties": {
       "location": {
         "type": "geo_point"
       },
       "entry": {
         "type": "keyword"
       },
       "exit_only": {
         "type": "keyword"
       }
     }
   }
 }
}
```

Add the pipeline:
```
PUT _ingest/pipeline/parse_nyc_csv
{
 "description": "Parsing the NYC stations",
 "processors": [
   {
     "grok": {
       "field": "station",
       "patterns": [
         "%{WORD:division},%{DATA:line},%{DATA:station_name},%{NUMBER:location.lat},%{NUMBER:location.lon},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA},%{DATA:entrance_type},%{DATA:entry},%{DATA:exit_only},%{DATA:vending}"
       ]
     }
   },
   {
     "remove": {
       "field": "station"
     }
   }
 ]
}
```

Index the data using both the pipeline and the bulk API:

```
curl -H "Content-Type: application/json" -XPOST "http://localhost:9200/subway_info_v2/station/_bulk?pipeline=parse_nyc_csv&pretty" --data-binary "@nyc-100.json"
```

Check that data was correctly imported:
```
GET subway_info_v2/_search
{
  "query": {
    "match_all": {}
  }
}
```

Based on:

https://www.elastic.co/blog/indexing-csv-elasticsearch-ingest-node


