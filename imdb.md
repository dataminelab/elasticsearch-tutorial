# IMDB movies analysis

## Import the data

```
curl -H "Content-Type: application/json" -XPOST "http://localhost:9200/imdb/default/_bulk?pretty" --data-binary "@imdb.json"
```

## Check mapping
```
GET imdb/default/_mapping
```

## Task: Add custom mapping for IMDB
* Review each field and make a decision on what should be changed and why

## Analyzers

```
POST _analyze
{
  "analyzer": "standard",
  "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
}

POST _analyze
{
  "tokenizer" : "keyword",
  "filter" : ["lowercase"],
  "char_filter" : ["html_strip"],
  "text" : "this is a <b>test</b>"
}
```

## Diactritics

```
DELETE my_index

PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "folding": {
          "tokenizer": "standard",
          "filter":  [ "lowercase", "asciifolding" ]
        }
      }
    }
  }
}

POST /my_index/_analyze
{
  "analyzer": "folding",
  "text": "My œsophagus caused a débâcle"
}

## To retain original text for the search consider storing it twice

DELETE /my_index
PUT /my_index/_mapping/my_type
{
  "properties": {
    "title": { 
      "type":           "text",
      "analyzer":       "standard",
      "fields": {
        "folded": { 
          "type":       "text",
          "analyzer":   "folding"
        }
      }
    }
  }
}

# title will contain the original text
# title.folded will have diactritics removed

PUT /my_index/my_type/1
{ "title": "Esta loca!" }

PUT /my_index/my_type/2
{ "title": "Está loca!" }

GET /my_index/_search
{
  "query": {
    "multi_match": {
      "type":     "most_fields",
      "query":    "esta loca",
      "fields": [ "title", "title.folded" ]
    }
  }
}
```

Alternative is to use `preserve_original` from `asciifolding` filter, but storing it separately is a cleaner solution.

## Tokenizers

See: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html
```
# standard, letter, whitespace, ngram
# pangram sentence, contains all letter of the alphabet
POST _analyze
{
  "tokenizer": {
  	"type": "ngram",
  	"min_gram": 1,
  	"max_gram": 2,
  	"token_chars": [
      "letter",
      "digit"
    ]
  },
  "text": "The quick brown fox jumps over the lazy dog."
}
```

# Analyzer

## Sample analyzer
```
DELETE /my_index
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": ["html_strip"],
          "filter": ["lowercase", "stemmer_en"]
        }
      }, 
      "filter": {
        "stemmer_en": {
          "type": "stemmer",
          "name": "english"
        }
      }
    }
  }
}

POST /my_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "The 2 <strong>QUICK</strong> Brown-Foxes jumped over the <i>lazy</i> dog's bone."
}
```

## Task

Add a custom char_filter called "emoticons", which will replace:
* :) with the _happy_face_
* :( with the _sad_face_

## Use the following template
```
PUT my_index
{
  "settings": {
    "analysis": {
      "char_filter": {
        ...
      }
    }
  }
}
```

## See what inverted index will be created
```
POST my_index/_analyze
{
  "tokenizer" : "standard",
  "char_filter" : ["emoticons"],
  "text" : "He who controls the spice, controls the universe :), Dune"
}
```

## Add the analyzer to the index mapping
```
PUT my_index/_mapping/my_type
{
  "properties": {
    "text": {
      "type":      "string",
      "analyzer":  "my_custom_analyzer"
    }
  }
}
```


## Task

Add custom analyzer to the IMDB mapping and reimport the data.

Extract length of the movie (in minutes) from the duration field.

Hint, use: pattern analyzer:
https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-pattern-analyzer.html

```
PUT imdb
{
  "settings": {
    "analysis": {
      "analyzer": {
        ...
      }
    }
  }
}

PUT imdb/_mapping/default
{
  "default": {
    "properties": {
 
        ...

    "duration": {
      "type": "text",
      "analyzer": "..."
    },
...

# Test that it works

POST imdb/default/_search
{
  "query": {
    "match": {
      "duration": "110"
    }
  }
}
```


## Task: Adding synonyms

```
Task:

# Create a synonym file with actor names
Brad Pitt,William Bradley Pitt
Meat Loaf,Michael Lee Aday
Tom Hanks,Thomas Jeffrey Hanks
John Travolta,John Joseph Travolta
Uma Thurman,Uma Karuna Thurman
```

Apply this to the IMDB mapping. Test with the simply search
query that it works correctly.

```
POST imdb/default/_search
{
  "query": {
    "match": {
      "actors": "Ellen Grace Philpotts-Page"
    }
  }
}
```

## Search

```
POST imdb/default/_search?explain
{
  "query": {
    "match": {
      "actors": "Leonardo DiCaprio"
    }
  }
}

# see _explanation
```

## Term query
```
GET index/default/_search
{
  "query": {
    "term" : { "actors.keyword" : "Uma Thurman" } 
  }
}

# Question, why this doesn't work?
GET imdb/default/_search
{
  "query": {
    "term" : { "actors" : "Uma Thurman" } 
  }
}

GET /imdb/default/_search
{
    "query": {
        "constant_score" : {
            "filter" : {
                "terms" : { "actors" : ["Uma Thurman", "John Travolta"]}
            }
        }
    }
}

# Filtering
GET /imdb/default/_search
{
    "query": {
        "constant_score" : {
            "filter" : {
                "terms" : { "actors.keyword" : ["Uma Thurman", "John Travolta"]}
            }
        }
    }
}

# Range queries
GET /imdb/default/_search
{
    "query": {
        "range" : {
            "imdbRating" : {
                "gte" : 9
           }
        }
    }
}

# Date range queries
GET /imdb/default/_search
{
    "query": {
        "range" : {
            "year" : {
                "gte" : "2016",
                "lt" :  "now/d",
                "format": "yyyy"

            }
        }
    }
}

# Exists
GET /imdb/default/_search
{
    "query": {
        "exists" : { "field" : "ratings" }
    }
}


# Wildcard queries
GET /imdb/default/_search
{
    "query": {
        "wildcard" : { "actors" : "T* Hanks" }
    }
}

```

## More like this query

```
# Using text as a template
GET /imdb/default/_search
{
    "_source": "originalTitle", 
    "query": {
        "more_like_this" : {
            "fields" : ["originalTitle"],
            "like" : ["The Godfather"],
            "min_term_freq" : 1,
            "min_doc_freq": 1,
            "minimum_should_match": "10%"
        }
    }
}

# Using existing document as a tempalte
GET /imdb/default/_search
{
    "_source": "originalTitle", 
    "query": {
        "more_like_this" : {
            "fields" : ["originalTitle"],
            "like" : [
              {
                  "_index" : "imdb",
                  "_type" : "default",
                  "_id" : "AV-iApAKI7QD-2E8QIsO"
              }
            ],
            "min_term_freq" : 1,
            "min_doc_freq": 1,
            "minimum_should_match": "10%"
        }
    }
}
```

## Suggesters
```
# Term suggester
POST imdb/_search
{
  "suggest": {
    "my-suggestion" : {
      "text" : "godfater",
      "term" : {
        "field" : "originalTitle"
      }
    }
  }
}

# see for more info:
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters-term.html

# It requires some changes in the mapping
DELETE imdb
PUT imdb/
{
  "mappings": {
    "default": {
      "properties": {
        "originalTitle": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            },
            "suggest": {
              "type": "completion"
            }
          }
        }
      }
    }
  }
}

# Reimport the data
# Movie suggest query
POST imdb/_search
{
    "_source": "originalTitle", 
    "suggest": {
        "movie-suggest" : {
            "prefix" : "The G", 
            "completion" : { 
                "field" : "originalTitle.suggest" 
            }
        }
    }
}
```

## Tasks: 
* find all "Lord of the Ring" movies using prefix query
* find all documents with "Lord of the Ring" multi match
  boost title and originalTitle * 3, and storyline * 1
* Which hotels have swimming pools and cost less than X per night?

# see blogs.md

## Aggregations

Calculate average rating across all movies
```
POST /imdb/default/_search?size=0
{
    "aggs" : {
        "avg_rating" : { "avg" : { "field" : "ratings" } }
    }
}
```

Rating statistics
```
POST /imdb/default/_search?size=0
{
    "aggs" : {
        "stats_rating" : { "stats" : { "field" : "ratings" } }
    }
}
```

Movie genres
```
GET /imdb/default/_search
{
    "size" : 0,
    "aggs" : {
        "genres" : {
            "terms" : { 
              "field" : "genres",
              "missing" : "N/A",
              "min_doc_count" : 0,
              "size" : 5
            }
        }
    }
}
```

## Subaggregation
```
GET /imdb/default/_search
{
  "size": 0,
  "query": {
    "range": {
      "year": {
        "gte": 2000
      }
    }
  },
  "aggs": {
    "genres_terms": {
      "terms": { "field": "genres" },
      "aggs": {
        "genres_stats": {
          "stats": { "field": "ratings" }
        }
      }
    }
  }
}
```

Notes:
* doc_count_error_upper_bound: an upper bound of the error on the document counts for each term
* sum_other_doc_count: when there are lots of unique terms, elasticsearch only returns the top terms; this number is the sum of the document counts for all buckets that are not part of the response

## Filter aggregation

See: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filter-aggregation.html
```
GET /imdb/default/_search
{
  "size": 0,
  "aggs": {
    "low_value": {
      "filter": {
        "range": {
          "imdbRating": {
            "gte": 6
          }
        }
      }
    }
  }
}
```

## Task

* How many movies there were before 1990, 1990-2000, 2000+
See: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-daterange-aggregation.html

* Create a histogram of movies by their rating (1-2, 2-3, ...)
See: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-histogram-aggregation.html

* Create a date-histogram of movies by their dates (10 years buckets)
See: 
* https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html
* https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units




