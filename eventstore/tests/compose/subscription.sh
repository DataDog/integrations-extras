#!/bin/sh

while ! curl -sS http://web:2113/info; do sleep 1; done
sleep 1
curl -sS -X PUT -d $'{"startFrom": 0,"resolveLinktos": false}' http://web:2113/subscriptions/newstream/examplegroup -u admin:changeit -H "Content-Type: application/json"
