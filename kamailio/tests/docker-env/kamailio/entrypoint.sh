#!/bin/sh

set -eu -o pipefail

if [ "$1" = "/usr/sbin/kamailio" ] || [ "$1" = "kamailio" ]; then
	chown -R root:kamailio /etc/kamailio/
	chown -R kamailio:kamailio /run/kamailio/
	chown -R dd-agent:dd-agent /opt/datadog-agent/
	chown -R root:root /etc/sudoers.d/
	find /opt/datadog-agent/scripts/ -type f -exec chmod 500 {} +;
fi

exec "$@"
