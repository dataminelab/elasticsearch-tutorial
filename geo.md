
## Geo

Define geo_point mapping:

```
 PUT stores
 PUT stores/_mapping/store
 {
   "store": {
     "properties": {
       "name": {
         "type": "keyword"
       },
       "address": {
         "type": "text"
       },
       "has_wifi" : {
         "type" : "boolean"
       },
       "location": {
         "type": "geo_point"
       }
     }
   }
 }
```

Add sample data:

```
#Index Stores
PUT stores/store/1
 {
   "name" : "Store1",
   "address" : "123 High Lane",
   "has_wifi" : true,
"location" : {
     "lat" : "37.339724",
     "lon" : "-121.873848"
   }
 }

 PUT stores/store/2
 {
   "name" : "Store2",
   "address" : "124 High Lane",
   "has_wifi" : true,
"location" : {
     "lat" : "37.338495",
     "lon" : "-121.880736"
   }
 }
```

Geo distance query:

```
POST stores/store/_search
  {
    "query": {
      "geo_distance": {
           "distance": "1mi",
           "location": {
           "lat": "37.348929",
           "lon": "-121.888536"
        }
      }
    }
  }
```

Sorting by GEO distance:

```
 POST stores/store/_search
 {
   "query": {
     "match_all": {}
   },
   "sort": [
     {
       "_geo_distance": {
         "location": {
           "lat": "37.348929",
           "lon": "-121.888536"
         },
         "order": "asc",
         "unit" : "mi"
       }
     }
   ]
 }
```