#!/bin/bash

go get -v github.com/nats-io/go-nats-streaming
go run /go/src/github.com/nats-io/go-nats-streaming/examples/stan-bench/main.go -s nats://nats_primary:4222 -n 10 test.channel1
go run /go/src/github.com/nats-io/go-nats-streaming/examples/stan-bench/main.go -s nats://nats_primary:4222 -n 10 test.channel2
go run /go/src/github.com/nats-io/go-nats-streaming/examples/stan-bench/main.go -s nats://nats_primary:4222 -n 10 test.channel3
sleep infinity

