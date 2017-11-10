
PUT imdb

Mapping for IMDB
```
PUT imdb/_mapping/default
{
  "default": {
    "properties": {
      "actors": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 100
          }
        }
      },
      "averageRating": {
        "type": "scaled_float",
        "scaling_factor": 100
      },
      "contentRating": {
        "type": "byte"
      },
      "duration": {
        "type": "keyword"
      },
      "genres": {
        "type": "keyword"
      },
      "imdbRating": {
        "type": "scaled_float",
        "scaling_factor": 100
      },
      "originalTitle": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "poster": {
        "type": "text",
        "index" : false,
        "store": false
      },
      "posterurl": {
        "type": "text",
        "index" : false
      },
      "ratings": {
        "type": "byte"
      },
      "releaseDate": {
        "type": "date",
        "format": "yyyy-MM-dd"
      },
      "storyline": {
        "type": "text"
      },
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "year": {
        "type": "date",
        "format": "year"
      }
    }
  }
}
```

Emojis

```
PUT my_index
{
  "settings": {
    "analysis": {
      "char_filter": {
        "emoticons": { 
          "type": "mapping",
          "mappings": [
            ":) => _happy_face_",
            ":( => _sad_face_"
          ]
        }
      }
    }
  }
}

POST my_index/_analyze
{
  "tokenizer" : "standard",
  "char_filter" : ["emoticons"],
  "text" : "He who controls the spice, controls the universe :), Dune"
}
```

## Task: Add custom mapping
```
PUT imdb
{
  "settings": {
    "analysis": {
      "analyzer": {
        "extract_numbers": {
          "type": "pattern",
          "pattern": "([^\\d]+)"
        },
        "synonym-actors": {
          "tokenizer": "standard",
          "ignore_case" : "true",
          "filter": ["lowercase", "actor_synonyms"]
        }
      },
      "filter" : {
        "actor_synonyms" : {
          "type" : "synonym",
          "synonyms" : [
            "Ellen Grace Philpotts-Page, Ellen Philpotts-Page, Ellen Page=>Ellen Page",
            "Brad Pitt,William Bradley Pitt",
            "Meat Loaf,Michael Lee Aday=>Meat Loaf",
            "Tom Hanks,Thomas Jeffrey Hanks",
            "John Travolta,John Joseph Travolta",
            "Uma Thurman,Uma Karuna Thurman"
          ]
        }
      }
    }
  }
}

# Test the extract analyzer
POST imdb/_analyze
{
  "analyzer": "extract_numbers",
  "text": "PT120M"
}

PUT imdb/_mapping/default
{
  "default": {
    "properties": {
      "actors": {
        "type": "text",
        "analyzer": "synonym-actors",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 100
          }
        }
      },
      "averageRating": {
        "type": "long"
      },
      "contentRating": {
        "type": "byte"
      },
      "duration": {
        "type": "text",
        "analyzer": "extract_numbers"
      },
      "genres": {
        "type": "keyword"
      },
      "imdbRating": {
        "type": "float"
      },
      "originalTitle": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "poster": {
        "type": "text",
        "index" : false
      },
      "posterurl": {
        "type": "text",
        "index" : false
      },
      "ratings": {
        "type": "byte"
      },
      "releaseDate": {
        "type": "date",
        "format": "yyyy-MM-dd"
      },
      "storyline": {
        "type": "text"
      },
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "year": {
        "type": "date",
        "format": "year"
      }
    }
  }
}

# Test it
POST imdb/default/_search
{
  "query": {
    "match": {
      "duration": "110"
    }
  }
}
```

# Custom analyzer
```
# custom analyzer with few filters and a stemmer
DELETE my_index

PUT my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom",
          "char_filter": [ "html_strip", "emoticons" ],
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "stop",
            "stemmer"
          ]
        }
      },
      "char_filter": {
        "emoticons": { 
          "type": "mapping",
          "mappings": [
            ":) => _happy_face_",
            ":( => _sad_face_"
          ]
        }
      }
    }
  }
}
```


## Find prefix movies
```
# Prefix (not analyzed, matches keywords)
GET /imdb/default/_search
{ "query": {
    "prefix" : { "originalTitle.keyword" : "The Lord" }
  }
}
```

## Mult-match with boosting
```
GET /imdb/default/_search
{
  "query": {
    "multi_match" : {
      "query": "Lord of the Ring",
      "fields": [ "title^3", "originalTitle^3", "storyline" ]
    }
  }
}
```

# Blogs

## Blogs nested mapping

Note: colons ":" in the name of the fields are not well supported!

```
PUT blogs
{
    "mappings": {
      "default": {
        "properties": {
          "_links": {
            "properties": {
              "about": {
                "properties": {
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "author": {
                "properties": {
                  "embeddable": {
                    "type": "boolean"
                  },
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "collection": {
                "properties": {
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "curies": {
                "properties": {
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  },
                  "name": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  },
                  "templated": {
                    "type": "boolean"
                  }
                }
              },
              "replies": {
                "properties": {
                  "embeddable": {
                    "type": "boolean"
                  },
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "self": {
                "properties": {
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "version-history": {
                "properties": {
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "wp_attachment": {
                "properties": {
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "wp_featuredmedia": {
                "properties": {
                  "embeddable": {
                    "type": "boolean"
                  },
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "wp_term": {
                "type": "nested",
                "properties": {
                  "embeddable": {
                    "type": "boolean"
                  },
                  "href": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  },
                  "taxonomy": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              }
            }
          },
          "author": {
            "type": "long"
          },
          "categories": {
            "type": "long"
          },
          "comment_status": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "content": {
            "properties": {
              "protected": {
                "type": "boolean"
              },
              "rendered": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          },
          "date": {
            "type": "date"
          },
          "date_gmt": {
            "type": "date"
          },
          "excerpt": {
            "properties": {
              "protected": {
                "type": "boolean"
              },
              "rendered": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          },
          "featured_media": {
            "type": "long"
          },
          "format": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "guid": {
            "properties": {
              "rendered": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          },
          "id": {
            "type": "long"
          },
          "link": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "modified": {
            "type": "date"
          },
          "modified_gmt": {
            "type": "date"
          },
          "ping_status": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "slug": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "status": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "sticky": {
            "type": "boolean"
          },
          "tags": {
            "type": "long"
          },
          "template": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "title": {
            "properties": {
              "rendered": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          },
          "type": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    }
  }
```

And the query:
```
GET blogs/default/_search
{
  "query": {
    "nested": {
      "path": "_links.wp_term",
      "query": {
        "bool": {
          "must": [
            { "match": { "_links.wp_term.taxonomy": "category" }},
            { "match": { "_links.wp_term.embeddable": false }}
          ]
        }
      }
    }
  }
}
```

## Fuzzy search
```
GET /blogs/default/_search
{
    "_source": ["title.rendered"],
    "query": {
        "match" : {
            "title.rendered" : {
                "query" : "undersstanding",
                "fuzziness" : "auto"
            }
        }
    },
    "highlight" : {
        "fields" : {
            "title.rendered" : {}
        }
    }
}
```

Geo query
```
GET /hotels/default/_search
{
    "query": {
        "bool" : {
            "must" : {
                "match_all" : {}
            },
            "filter" : {
                "geo_distance" : {
                    "distance" : "2km",
                    "location" : {
                        "lat" : 37.556035,
                        "lon" : 127.005232
                    }
                }
            }
        }
    }
}
```


## How many movies there were before 1990, 1990-2000, 2000+

```
POST /imdb/default/_search?size=0
{
    "aggs": {
        "range": {
            "date_range": {
                "field": "year",
                "ranges": [
                    { "to": "1990" }, 
                    { "from": "1990", "to": "2000" }, 
                    { "from": "2000" }
                ]
            }
        }
    }
}
```

## Create a histogram of movies by their rating (1-2, 2-3, ...)
```
POST /imdb/default/_search?size=0
{
    "aggs" : {
        "prices" : {
            "histogram" : {
                "field" : "imdbRating",
                "interval" : 1,
                "min_doc_count" : 0
            }
        }
    }
}
```

## Create a date-histogram of movies by their dates (1 year buckets)
```
POST /imdb/default/_search?size=0
{
    "aggs" : {
        "movies_over_time" : {
            "date_histogram" : {
                "field" : "year",
                "interval" : "year"
            }
        }
    }
}
```




