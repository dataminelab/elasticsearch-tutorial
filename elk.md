# ELK

First install filebeat and logstash:

## Logstash
https://www.elastic.co/downloads/logstash
```
wget https://artifacts.elastic.co/downloads/logstash/logstash-5.6.4.tar.gz
tar xzvf logstash-5.6.4.tar.gz
cd ./logstash-5.6.4
# update config/logstash.yml and pipeline/logstash.conf
# see for a reference
https://github.com/dataminelab/elasticsearch-tutorial/blob/master/docker-elk/logstash/config/logstash.yml

# Example
mkdir pipeline
cd pipeline
# use config from here:
# change "elasticsearch:9200" to your elasticsearch, e.g.: "localhost:9200"
https://github.com/dataminelab/elasticsearch-tutorial/blob/master/docker-elk/logstash/pipeline/logstash.conf


http.host: "127.0.0.1"
# folder from the pipeline above
path.config: /absolute/path/to/your/pipeline

# start
./bin/logstash
```

Default config:
```
http.host: "127.0.0.1"
path.config: /your/home/folder
```

## Filebeat
https://www.elastic.co/downloads/beats/filebeat
(no need to configure for now)

```
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-5.6.4-linux-x86.tar.gz
tar xzvf filebeat-5.6.4-linux-x86.tar.gz
cd filebeat-5.6.4-linux-x86

# download and install dashboards (optional, do it only on your local/dev cluster)
# see for more info: https://www.elastic.co/guide/en/beats/filebeat/current/configuration-dashboards.html
wget https://artifacts.elastic.co/downloads/beats/beats-dashboards/beats-dashboards-5.6.4.zip
./scripts/import_dashboards -file ./beats-dashboards-5.6.4.zip  -es http://localhost:9200

# import the data
# Replace /var/logs/nginx_logs/nginx_logs to absolute path to
# https://github.com/dataminelab/elasticsearch-tutorial/blob/master/data/nginx_logs/nginx_logs
# download sample nginx logs data
wget https://github.com/dataminelab/elasticsearch-tutorial/blob/master/data/nginx_logs/nginx_logs
./filebeat -e --modules=nginx -M "nginx.access.var.paths=[/Users/radek/src/d/elasticsearch-tutorial/data/nginx_logs/nginx_logs]"

# Verify that it worked
curl http://localhost:9200/filebeat-*/_count
# should return a response a "count":51462
```

(Alternative) Docker AWS setup
```
# Create AWS `Amazon Linux` instance `t2.medium`
# install docker
sudo yum -y install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
# relogin
# install git
sudo yum -y install git
git clone https://github.com/dataminelab/elasticsearch-tutorial.git
cd elasticsearch-tutorial/docker-elk/
# install docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
# start docker containers
docker-compose up
# or run as a daemon: docker-compose up
# AWS configuration
# * open ports 9200 and 5601 on your IP address
# Wait few minutes (be patient)
```

## Add files to the index with the filebeat
```
# connect to filebeat docker
docker exec -it dockerelk_filebeat_1 bash
# Run filebeat
filebeat -e --modules=nginx --setup  -M "nginx.access.var.paths=[/var/logs/nginx_logs/nginx_logs]"
# Verify that it worked
curl http://localhost:9200/filebeat-*/_count
# should return a response a "count":51462
```

## UI

* Navigate to: http://localhost:5601
* Create index pattern (if asked): `filebeat-*`
* Go to dashboard, choose Nginx Logs (select last 5 years)

See:
* https://www.elastic.co/guide/en/elasticsearch/reference/5.6/query-dsl-query-string-query.html#query-string-syntax

References:
* https://github.com/elastic/examples/tree/master/Common%20Data%20Formats/nginx_logs