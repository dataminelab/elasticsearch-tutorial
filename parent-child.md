
## Parent-child mappings

Parent (article), child (comment)

```
PUT blog
 {
   "mappings": {
      "article": {
       "properties": {
         "title": {
           "type": "text"
         },
         "category": {
           "type": "keyword"
         }
       }
     },
     "comment": {
       "_parent": {
         "type": "article"
       },
       "properties": {
         "comment": {
           "type": "text"
         },
         "userid": {
           "type": "keyword"
         }
       }
     }
   }
 }
```

Add documents:

```
#Parent
PUT blog/article/1 
{
  "title" : "Hello world !!",
  "category" : "Introduction"
}

#Children
PUT blog/comment/10?parent=1
{
  "comment" : "This world is awesome",
  "userid" : "user1"
}
```

Querying with `has_child`.

Find all comments made by `user1`:

```
POST blog/article/_search
 {
   "query": {
     "has_child": {
       "type": "comment",
       "query": {
         "term": {
           "userid": "user1"
         }
       },
       "inner_hits": {}
     }
   }
 }
```

Querying with `has_parent`

Find all comments from introduction category:

```
POST blog/comment/_search
 {
   "query": {
    "has_parent": {
       "parent_type": "article",
       "query": {
         "term": {
           "category" : "Introduction"
         }
       }
     }
   }
 }
```

## Nested

Use `nested` mapping type:
```
#Delete existing index
DELETE products

#Set mappings
PUT products
 {
   "settings": {},
   "mappings": {
     "product": {
       "properties": {
         "product_name": {
           "type": "text",
           "copy_to": "product_suggest"
         },
         "variations": {
           "type": "nested",
           "properties": {
             "type": {
               "type": "keyword"
             },
             "value": {
               "type": "keyword"
             },
             "unit_price": {
               "type": "double"
             }
           }
         },
         "product_suggest": {
           "type": "completion"
         }
       }
     },
     "product_review": {
       "_parent": {
         "type": "product"
       },
       "properties": {}
     }
   }
 }
```

Index documents:
```
#Parent document with nested variations
PUT products/product/1?refresh=true
 {
   "product_name": "Apple iPhone 6",
   "variations": [ 
     {
       "type": "storage",
       "value": "16GB",
       "unit_price": "600"
     },
     {
       "type": "storage",
       "value": "64GB",
       "unit_price": "700"
     }
   ]
 }

 PUT products/product/2?refresh=true
 {
   "product_name": "Apple iPhone 7",
   "variations": [
     {
       "type": "storage",
       "value": "128GB",
       "unit_price": "900"
     }
   ]
 }

 #Child Document
 POST products/product_review/?parent=1
 {"user_id" : "reviewer1", "comment" : "One of the best phones in the market"}
```

Querying, find all documents matching both the parent and the nested documents:
```
#Nested Query (Query for iPhone with 128GB)
 POST products/product/_search
 {
   "query": {
     "bool": {
       "must": [
         {
           "term": {
             "product_name": "iphone"
           }
         },
         {
           "nested": {
             "path": "variations",
             "query": {
               "bool": {
                 "must": [
                   {
                     "term": {
                       "variations.type": "storage"
                     }
                   },
                   {
                     "term": {
                       "variations.value": "128GB"
                     }
                   }
                 ]
               }
             }
           }
         }
       ]
     }
   }
 }
```


Include inner_hits:
```
#Inner hits
POST products/product/_search
 {
  "_source": false,    
   "query": {
     "nested": {
       "path": "variations",
       "query": {
         "bool": {
           "must": [
             {
               "term": {
                 "variations.type": "storage"
               }
             },
             {
               "term": {
                 "variations.value": "64GB"
               }
             }
           ]
         }
       },
       "inner_hits": {}
     }
   }
 }
```

