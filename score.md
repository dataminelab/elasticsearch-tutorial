
## Relevance and scoring

Import test data:
```
PUT products
 {
   "settings": {},
   "mappings": {
     "product": {
       "properties": {
         "product_name": {
           "type": "text",
           "analyzer": "english"
         },
         "description" : {
           "type": "text",
           "analyzer": "english"
         }
       }
     }
   }
 }

PUT products/product/1
{
   "product_name": "Men's High Performance Fleece Jacket",
   "description": "Best Value. All season fleece jacket",
   "unit_price": 79.99,
   "reviews": 250,
   "release_date": "2016-08-16"
 } 
 
PUT products/product/2
{
   "product_name": "Men's Water Resistant Jacket",
   "description": "Provides comfort during biking and hiking",
   "unit_price": 69.99,
   "reviews": 5,
   "release_date": "2017-03-02"
 } 
 
PUT products/product/3
{
   "product_name": "Women's wool Jacket",
   "description": "Helps you stay warm in winter",
   "unit_price": 59.99,
   "reviews": 10,
   "release_date": "2016-12-15"
 }

```

Constant score filter:
```
POST products/_search
 {
   "query": {
     "constant_score": {
       "filter": {
         "term" : {
           "product_name" : "wool"
         }
       }
     }
   }
 }
```

Bool query with both the query and filter contexts:

```
POST products/_search
 {
   "query": {
     "bool": {
       "must": [
         {
           "match": {
             "product_name": "jacket"
           }
         },
         {
           "constant_score": {
             "filter": {
               "range": {
                 "unit_price": {
                   "lt": "100"
                 }
               }
             }
           }
         }
       ]
     }
   }
 }
```

Use field_value_factor:

```
POST products/_search
 {
   "query": {
     "function_score": {
       "query": { 
         "match": {
           "product_name" : "jacket"
         }
       },
       "field_value_factor": { 
         "field": "reviews",
         "factor": "0.25"
       }
     }
   }
 }
```

Score will be calculated as:
```
score = _score + (factor * reviews)
```

Combining bool queries:
* results must match the `must` query
* `should` queries will influence the score. The more `should` clauses matched the higher the score
* Note `range` query increases each matched document score by `1`

```
#Boosting queries using bool
POST products/_search
 {
   "query": {
     "bool": {
       "must": [
         {
           "match": {
             "product_name": "jacket"
           }
         }
       ],
       "should": [
         {
           "range": {
             "unit_price": {
               "lt": 100
             }
           }
         },
         {
           "range": {
             "reviews": {
               "gte": 25
             }
           }
         }
       ]
     }
   }
 }
```

Rescoring example:
```
POST products/_search
 {
   "query": {
     "match": {
       "product_name": {
         "query": "jacket"
       }
     }
   },
   "rescore": {
     "window_size": 10,
     "query": {
       "rescore_query": {
         "function_score": {
           "script_score": {
             "script": {
               "source": "Math.log(params['_source']['reviews'])"
             }
           }
         }
       },
       "query_weight": 0.5,
       "rescore_query_weight": 1.0
     }
   }
 }
```

Debugging:
```
POST products/_search?explain
 {
   "query": {
     "match": {
       "description" : "hiking"
     }
   }
 }
```

Source:
https://www.packtpub.com/mapt/book/big_data_and_business_intelligence/9781787128453/6/ch06lvl1sec46/relevance