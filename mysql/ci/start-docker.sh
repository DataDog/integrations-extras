#!/bin/bash

NAME='dd-test-mysql'

set -e

PORT=13306

if docker ps | grep dd-test-mysql >/dev/null; then
  echo 'the containers already exist, we have to remove them'
  bash mysql/ci/stop-docker.sh
fi

MYSQL00_ID=$(docker run -p 3306:3306 --name $NAME -e MYSQL_ROOT_PASSWORD=datadog -d mysql:5.7)
MYSQL00_IP=$(docker inspect ${MYSQL00_ID} | grep '"IPAddress"' | cut -d':' -f2 | cut -d'"' -f2)
MYSQL00_IP=$(echo $MYSQL00_IP | cut -d " " -f2)

until [[ `docker logs dd-test-mysql 2>&1` =~ .*"MySQL init process done. Ready for start up".*"ready for connections".* ]];
do
  # docker logs dd-test-mysql
  sleep 2
done

# docker logs dd-test-mysql


docker run -it --link dd-test-mysql:mysql --rm mysql:5.7 sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" -e "create user \"dog\"@\"%\" identified by \"dog\"; GRANT PROCESS, REPLICATION CLIENT ON *.* TO \"dog\"@\"%\" WITH MAX_USER_CONNECTIONS 5; CREATE DATABASE testdb; CREATE TABLE testdb.users (name VARCHAR(20), age INT); GRANT SELECT ON testdb.users TO \"dog\"@\"%\"; INSERT INTO testdb.users (name,age) VALUES(\"Alice\",25); INSERT INTO testdb.users (name,age) VALUES(\"Bob\",20); GRANT SELECT ON performance_schema.* TO \"dog\"@\"%\"; USE testdb; SELECT * FROM users ORDER BY name; "'
