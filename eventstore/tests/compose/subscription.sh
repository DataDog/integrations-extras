#!/bin/sh

# Wait for the server to come up
while ! curl -sS http://web:2113/info; do sleep 1; done; echo

# Wait for the cluster quorum
while curl -sS http://web:2113/info | grep -F state | grep -Evq 'master|slave|clone|readonlyreplica'; do sleep 1; done

# Wait for the auth module to initialize
while test "$(curl -sS -o /dev/null -u admin:changeit -w '%{http_code}' http://web:2113/info/options)" != "200"; do sleep 1; done

# Display the node state for reference
curl -sS http://web:2113/info; echo

# Create the test subscription to fetch metrics from
curl -sS -X PUT -d $'{"startFrom": 0,"resolveLinktos": false}' http://web:2113/subscriptions/newstream/examplegroup -u admin:changeit -H "Content-Type: application/json"
