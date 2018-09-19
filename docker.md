
Download and run dockerised Elasticsearch:

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2

docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

Elasticsearch with Kibana:

See `docker-compose.yml` for a reference. 
To start elasticsearch together with Kibana simply type:
```
docker-compose up
```
Then visit:
http://localhost:5601

For more details see:
* https://www.elastic.co/guide/en/elasticsearch/reference/6.3/docker.html
* https://www.docker.elastic.co/