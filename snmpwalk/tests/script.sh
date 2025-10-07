#!/bin/bash
docker exec docker_snmpd_1 /usr/bin/snmpwalk "$@"
