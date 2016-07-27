#!/bin/bash

set -e

if docker ps | grep dd-test-mongo >/dev/null 2>&1; then
  containers=`docker ps --format '{{.Names}}' | grep dd-test-mongo`

  echo 'removing containers'
  for container in $containers; do
    echo "removing $container"
    docker kill $container >/dev/null 2>&1
    docker rm $container >/dev/null 2>&1
  done

fi
