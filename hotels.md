
## Create Index
```
PUT hotels
```

## Create index with shards and replicas

```
DELETE hotels

curl -XPUT 'localhost:9200/hotels?pretty' -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "index" : {
            "number_of_shards" : 3, 
            "number_of_replicas" : 2 
        }
    }
}
'
```

## Without curl, using Kibana

```
PUT hotels?pretty
{
    "settings" : {
        "index" : {
            "number_of_shards" : 3, 
            "number_of_replicas" : 2 
        }
    }
}
```

## List indexes
```
GET /_cat/indices?v
```

## Import sample data

```
POST hotels/default/1
{
    "type" : "hotel",
    "name" : "Motif Seattle",
    "city" : "Seattle",
    "countryCode" : "US",
    "hotelRating" : 4,
    "location" : {
      "lat" : 47.60985,
      "lon" : -122.33475
    }
}
GET hotels/default/1
```

## Update the existing record

```
PUT hotels/default/1
{
    "type" : "hotel",
    "name" : "Motif Seattle",
    "city" : "Seattle",
    "countryCode" : "US",
    "hotelRating" : 4,
    "location" : {
      "lat" : 47.60985,
      "lon" : -122.33475
    }
}
```


## Search all data
```
POST hotels/default/_search
```

## Simple search
```
GET /hotels/default/_search
{
    "query": {
        "match" : {
           "name" : "Motif"
        }
    }
}
```

## Partial update
```
POST /hotels/default/1/_update
{
   "doc" : {
       "name" : "Motif",
       "hotelRating": 3
   }
}
```

## Scripted partial update
```
POST /hotels/default/1/_update
{
   "script" : "ctx._source.hotelRating += 1" 
}
```

## Upsert
```
POST /hotels/default/2/_update
{
    "script" : {
        "source": "ctx._source.hotelRating = params.rating",
        "lang": "painless",
        "params" : {
            "rating" : 4
        }
    },
    "upsert" : {
        "hotelRating" : 1
    }
}
GET hotels/default/2
```

## Deleting documents
```
DELETE /hotels/default/2
```

## Delete by query
```
POST hotels/_delete_by_query
{
  "query": { 
    "match": {
      "name": "Motif"
    }
  }
}
```

## Bulk import all data

See: https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html

```
curl -H "Content-Type: application/json" -XPOST "http://localhost:9200/hotels/default/_bulk?pretty" --data-binary "@hotels.json"
```

Notes:
If you have existing JSON file that needs converting to NDJSON, there are few solutions:
* https://github.com/mradamlacey/json-to-es-bulk
* https://stedolan.github.io/jq/

## Check cluster health
```
GET _cluster/health
```

##
```
# Displays all commands
GET /_cat

# Health
GET /_cat/health
# Use format=json if preffered
GET /_cat/health?format=json
# Each command accepts help
GET /_cat/health?help

# Display results with column headers (verbose)
GET /_cat/nodes?v

# List indices
GET /_cat/indices?v

# Shards allocation
GET /_cat/allocation?v
```

## Assignment

* Create index `products` with 2 replicas and 5 shards
* Bulk import 3-5 hotels with following fields:
type, name, city, countryCode, hotelRating
* Delete 1 hotel
* Upsert 1 hotel (change name)


## Recreate index with the mapping

```
# Check existing mapping and compare it with the new one
GET hotels/default/_mapping

# Delete and recreate the mapping

DELETE /hotels

PUT hotels/
{
  "mappings" : {
    "default" : {
      "properties" : {
        "name": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
        "stars" : { "type" : "byte" },
        "rooms" : { "type" : "short" },
        "location" : { "type" : "geo_point" },
        "city" : { "type" : "keyword" },
        "address": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
        "internet" : { "type" : "boolean" },
        "service" : { "type" : "keyword" },
        "checkin": { "type" : "date", "format" : "dateOptionalTime"}
      }
    }
  }
}

# Reimport the bulk data
```

## Testing _all field
```
GET hotels/default/_search
{
  "query": {
    "match": {
      "_all": "Seoul"
    }
  }
}
```

## Disable dynamic mappings

```
PUT /hotels/_mapping/default
{
  "dynamic": "strict"
}

# test it
POST hotels/default/1
{
    "type3" : "hotel"
}
```

## Task - Geo query
Find all hotels in 2 km radius from the
point: 37.556035, 127.005232
(latitude, longitude)

## Sorting and pagination

```
GET /hotels/default/_search
{
    "sort" : [
       { "price" : {"order" : "asc" } },
        "_score"
    ],
    "query" : {
        "term" : { "service" : "spa" }
    }
}
```

# Aggregations

## Filters aggregation

See: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filters-aggregation.html
```
GET hotels/default/_search
{
  "size": 0,
  "aggs" : {
    "messages" : {
      "filters" : {
        "filters" : {
          "spas" :   { "match" : { "service" : "spa"   }},
          "weddings" : { "match" : { "service" : "wedding" }}
        }
      }
    }
  }
}
```

## Range aggregation

See: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-range-aggregation.html

```
GET hotels/default/_search
{
  "size": 0,
  "aggs" : {
        "price_ranges" : {
            "range" : {
                "field" : "price",
                "ranges" : [
                    { "to" : 150 },
                    { "from" : 150, "to" : 200 },
                    { "from" : 250, "to" : 300 },
                    { "from" : 300 }
                ]
            }
        }
    }

}
```


References:
* Data source: https://github.com/wikibook/elasticsearch

