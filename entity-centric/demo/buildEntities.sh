echo "Indexing reviewer entity profiles from review event data"
es_host="http://localhost:9200"
updateScriptID=ReviewerProfileUpdater


curl -X DELETE "$es_host/reviewers"
curl -XPUT    "$es_host/reviewers" -d '
{
   "settings" : {
        "number_of_shards" : 1,
        "number_of_replicas" : 0
    },
	"mappings":{
      "reviewer": {
        "properties": {
          "avgRating": {
            "type": "float"
          },
          "numVendors": {
            "type": "long"
          },
          "profile": {
            "type": "keyword"
          },
          "vendors": {
            "properties": {
              "num_ratings": {
                "type": "long"
              },
              "total_rating": {
                "type": "long"
              },
              "vendorId": {
                "type": "keyword"
              }
            }
          }
        }
      }
    }
}    
'
python ../ESEntityCentricIndexing.py anonreviews review eventQuery.json reviewerId reviewers reviewer $updateScriptID -scriptMode incremental
