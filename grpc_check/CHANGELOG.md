# CHANGELOG - gRPC Check


## 1.1.1 / 2026-05-05

***Fixed***:

* Fix unbounded growth of tag lists on every collection run (aliases and appends to instance `tags`) causing linear Agent CPU/memory growth (AGENT-16111) ([#2991](https://github.com/DataDog/integrations-extras/pull/2991))
* Reuse a single gRPC channel across check runs instead of opening and closing a channel every interval; RPC header interceptors are built once at init ([#2991](https://github.com/DataDog/integrations-extras/pull/2991))

## 1.1.0 / 2026-01-16

***Added***:

* Add option to force creation of secure channel ([#2883](https://github.com/DataDog/integrations-extras/pull/2883))

## 1.0.2 / 2022-11-09

***Fixed***:

* Fix timeout default value ([#1601](https://github.com/DataDog/integrations-extras/pull/1601))

## 1.0.1 / 2022-08-02
