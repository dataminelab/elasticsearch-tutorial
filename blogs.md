
## Blog examples

## Define the mapping and import the data

Bulk import the data
```
curl -H "Content-Type: application/json" -XPOST "http://localhost:9200/blog/default/_bulk?pretty" --data-binary "@blog.json"
```

## Check the mapping
```
GET blogs/_mapping
```

## Bool query with filtering
```
GET /_search
{
  "query": { 
    "bool": { 
      "must": [
        { "match": { "title.rendered": "Analytics" }} 
      ],
      "filter": [ 
        { "term":  { "status": "publish" }}, 
        { "range": { "date_gmt": { "gte": "2017-11-01" }}} 
      ]
    }
  }
}
```

## Proximity search

```
GET /blogs/default/_search
{
    "_source": ["content.rendered"],
    "query": {
        "match_phrase" : {
            "content.rendered" : {
                "query" : "user experience",
                "slop" : 1
            }
        }
    }
}
```


## Task: Fuzzy search

* Find blogs with titles containing word "undersstanding"
* Assume user did the mistake typing the keyword
* Return only the title and add highligting to it

## Nested sets

```
PUT my_index
{
  "mappings": {
    "default": {
      "properties": {
        "user": {
          "type": "nested" 
        }
      }
    }
  }
}

PUT my_index/default/1
{
  "group" : "fans",
  "user" : [
    {
      "first" : "John",
      "last" :  "Smith"
    },
    {
      "first" : "Alice",
      "last" :  "White"
    }
  ]
}

GET my_index/_search
{
  "query": {
    "nested": {
      "path": "user",
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "White" }} 
          ]
        }
      }
    }
  }
}
```

## Task: Nested data sets

* Create nested mapping for _links => wp_term
* Find documents which have taxonomy equal "category" and are not embeddable (false)


## References

* Data source: https://www.sitepoint.com/wordpress-json-example/
