
Create mapping for the data:
```
PUT /weather-data
{
  "mappings": {
    "state": {
      "properties": {
        "city":{
          "type": "text"
        },
        "date": {
          "type":   "date",
          "format": "dd-MM-yyyy"
        },
        "temp":{
          "type": "integer"
        }
      }
    }
  }
}
```

Import sample data:
```
curl -XPOST 'http://localhost:9200/weather_data/_bulk' --data-binary @data/weather-data.json
```

Average Bucket Aggregation (sibling aggregation):

Take the aggregated values from the "monthly_avg", in each bucket of "temp" and return the mean value.

```
POST /weather-data/_search?pretty
{
  "aggs": {
    "temp": {
      "date_histogram": {
        "field": "date",
        "interval": "month",
        "format": "dd-MM-yyyy"
      },
      "aggs": {
        "monthly_avg": {
          "avg": {
            "field": "temp"
          }
        }
      }
    },
    "avg_monthly_temp": {
      "avg_bucket": {
        "buckets_path": "temp>monthly_avg"
      }
    }
  }
}
```

Maximum/minimum aggregation:
```
POST /weather-data/_search?pretty
{
  "aggs": {
    "temp": {
      "date_histogram": {
        "field": "date",
        "interval": "month",
        "format": "dd-MM-yyyy"
      },
      "aggs": {
        "monthly_avg": {
          "avg": {
            "field": "temp"
          }
        }
      }
    },
    "max_monthly_average": {
	  "max_bucket": {
	    "buckets_path": "temp>monthly_avg"
	  }
	}
  }
}
```

Recreate the index with the mapping for weather related deaths:

```
DELETE /weather-data
PUT /weather-data
{
  "mappings": {
    "city": {
      "properties": {
        "city":{
          "type": "text"
        },
        "date": {
          "type":   "date",
          "format": "dd-MM-yyyy"
        },
        "temp":{
          "type": "integer"
        },
        "relatedDeaths":{
          "type": "integer"
        }
      }
    }
  }
}
```

Import sample data:
```
curl -XPOST 'http://localhost:9200/weather_data/_bulk' --data-binary @data/weather-deaths.json
```

Sum bucket aggregation.

Weather related deaths by month and total:

```
POST /weather-data/_search?pretty
{
  "query": {
    "match": {
      "city": "NY"
    }
  },
  "aggs": {
    "temp": {
      "date_histogram": {
        "field": "date",
        "interval": "month",
        "format": "dd-MM-yyyy"
      },
      "aggs": {
        "monthly": {
          "sum": {
            "field": "relatedDeaths"
          }
        }
      }
    },
    "sum_bucket_demo": {
      "sum_bucket": {
        "buckets_path": "temp>monthly"
      }
    }
  }
}
```

Monthly and total weather related deaths in NY:
```
POST /weather-data/_search?pretty
{
  "query": {
    "match": {
      "city": "NY"
    }
  },
  "aggs": {
    "temp": {
      "date_histogram": {
        "field": "date",
        "interval": "month",
        "format": "dd-MM-yyyy"
      },
      "aggs": {
        "monthly": {
          "sum": {
            "field": "relatedDeaths"
          }
        },
        "cumulative_demo": {
          "cumulative_sum": {
            "buckets_path": "monthly"
          }
        }  
      }
    }
  }
}
```

Cumulative sum aggregation:
```
POST /weather-data/_search?pretty
{
  "query": {
    "match": {
      "city": "NY"
    }
  },
  "aggs": {
    "temp": {
      "date_histogram": {
        "field": "date",
        "interval": "month",
        "format": "dd-MM-yyyy"
      },
      "aggs": {
        "monthly": {
          "sum": {
            "field": "relatedDeaths"
          }
        },
        "cumulative_demo": {
          "cumulative_sum": {
            "buckets_path": "monthly"
          }
        }  
      }
    }
  }
}
```

Based on: https://qbox.io/blog/introduction-pipeline-aggregations