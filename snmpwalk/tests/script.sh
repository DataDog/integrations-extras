#!/bin/bash
docker exec snmpwalk_snmpd /usr/bin/snmpwalk "$@"
