#!/bin/bash

set -e

if docker ps | grep dd-test-mongo >/dev/null; then
  containers=`docker ps --format '{{.Names}}' | grep dd-test-mongo`

  echo 'removing containers'
  for container in $containers; do
    echo "stopping $container"
    docker kill $container >/dev/null 2>&1
  done

  stopped_containers=`docker ps -a --format '{{.Names}}' | grep dd-test-mongo`
  for container in $stopped_containers; do
    echo "removing $container"
    docker rm $container >/dev/null 2>&1
  done

fi
