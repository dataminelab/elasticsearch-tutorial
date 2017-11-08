# ELK

(Optional) Docker AWS setup
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

TODO:
* Add few sample queries

References:
* https://github.com/elastic/examples/tree/master/Common%20Data%20Formats/nginx_logs