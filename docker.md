
The easiest way is to run Elasticsearch with Kibana using docker-compose:

See `docker-compose.yml` for a reference. 
To start elasticsearch together with Kibana simply type:
```
docker-compose up
```
Then visit:
http://localhost:5601


Alternatively download and run dockerised Elasticsearch:

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2

# create a network
docker network create mynet

docker run --name es --net mynet -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

And then download and run dockerised Kibana:
```
docker pull docker.elastic.co/kibana/kibana:6.3.2
docker run --net mynet -p 5601:5601 -e "ELASTICSEARCH_URL=http://es:9200" docker.elastic.co/kibana/kibana:6.3.2
```

For more details see:
* https://www.elastic.co/guide/en/elasticsearch/reference/6.3/docker.html
* https://www.docker.elastic.co/