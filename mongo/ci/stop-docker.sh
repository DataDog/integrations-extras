#!/bin/bash

set -e

docker kill dd-test-mongo
docker rm dd-test-mongo
docker kill dd-test-mongo-1
docker rm dd-test-mongo-1
docker kill dd-test-mongo-2
docker rm dd-test-mongo-2
