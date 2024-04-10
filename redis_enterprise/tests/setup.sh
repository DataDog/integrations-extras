#!/bin/bash

docker compose up -d

container_name="tests-redis-1"

echo "waiting for the servers..."
sleep 10
echo "creating cluster..."

while [[ "$(curl -o /dev/null  --cipher ECDHE-RSA-AES128-GCM-SHA256 -w ''%{http_code}'' -X POST -H 'Content-Type:application/json' -d '{"action":"create_cluster","cluster":{"name":"datadog.local"},"node":{"paths":{"persistent_path":"/var/opt/redislabs/persist","ephemeral_path":"/var/opt/redislabs/tmp"}},"credentials":{"username":"datadog@redis.com","password":"burythebone"}}' -k https://localhost:9443/v1/bootstrap/create_cluster)" != "200" ]]; do sleep 5; done

# test the cluster
while [[ "$(curl -o ./cluster -w ''%{http_code}'' -u datadog@redis.com:burythebone -k https://localhost:9443/v1/bootstrap)" != "200" ]]; do
  sleep 5;
done
echo "cluster..." && cat ./cluster
echo ""

# test the nodes
while [[ "$(curl -o ./nodes -w ''%{http_code}'' -u datadog@redis.com:burythebone -k https://localhost:9443/v1/nodes)" != "200" ]]; do
  sleep 5;
done
echo "nodes..." && cat ./nodes
echo ""


# create a user
while [[ "$(curl -o ./users -w ''%{http_code}'' -u datadog@redis.com:burythebone -X POST -H 'Content-Type: application/json' -d '{"email": "test@redis.com","password": "howtimeflies","name": "test","email_alerts": false,"role": "admin"}' -k https://localhost:9443/v1/users)" != "200" ]]; do
  sleep 5;
done
echo "users..." && cat ./users
echo ""

# add the database
while [[ "$(curl -o ./database -w ''%{http_code}'' -u datadog@redis.com:burythebone --location-trusted -H 'Content-type:application/json' -d '{ "name": "datadog", "port": 12000, "memory_size": 500000000, "type" : "redis", "replication": false }' -k https://localhost:9443/v1/bdbs)" != "200" ]]; do
  sleep 5;
done
echo "database..." && cat ./database
echo ""

# enable bdb name
docker exec -it "${container_name}" bash -c "/opt/redislabs/bin/ccs-cli hset cluster_settings metrics_exporter_expose_bdb_name enabled"
docker exec -it "${container_name}" bash -c "/opt/redislabs/bin/supervisorctl restart metrics_exporter"

# cleanup
rm cluster nodes users database

echo "waiting for metrics to be available"
sleep 50
echo "done"
