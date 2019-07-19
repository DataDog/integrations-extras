#!/bin/bash

apt-get update && apt-get install host -y
NATS_SERVER_IP=`host $NATS_SERVER | awk '{ print $4 }'`
NATS_CONNECTION_NAME=foo-sub /usr/local/bundle/bin/nats-sub foo -s http://$NATS_SERVER_IP:4222 &
/usr/local/bundle/bin/nats-sub bar -s http://$NATS_SERVER_IP:4222 &
/usr/local/bundle/bin/nats-pub foo "foo1" -s http://$NATS_SERVER_IP:4222
/usr/local/bundle/bin/nats-pub foo "foo2" -s http://$NATS_SERVER_IP:4222
/usr/local/bundle/bin/nats-pub bar "bar1" -s http://$NATS_SERVER_IP:4222
sleep infinity
