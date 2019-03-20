#!/bin/bash

NATS_CONNECTION_NAME=foo-sub /usr/local/bundle/bin/nats-sub foo -s http://$NATS_SERVER:4222 &
/usr/local/bundle/bin/nats-sub bar -s http://$NATS_SERVER:4222 &
/usr/local/bundle/bin/nats-pub foo "foo1" -s http://$NATS_SERVER:4222
/usr/local/bundle/bin/nats-pub foo "foo2" -s http://$NATS_SERVER:4222
/usr/local/bundle/bin/nats-pub bar "bar1" -s http://$NATS_SERVER:4222
sleep infinity
