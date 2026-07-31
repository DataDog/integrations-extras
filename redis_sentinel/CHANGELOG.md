# CHANGELOG - Redis Sentinel

## 1.2.0 / 2026-07-31

***Added***:

* Add SSL/TLS support (`ssl`, `ssl_certfile`, `ssl_keyfile`, `ssl_ca_certs`, `ssl_cert_reqs`, `ssl_check_hostname`) for connecting to TLS-enabled Sentinel instances ([#3071](https://github.com/DataDog/integrations-extras/pull/3071))
* Add `sentinel_username` for Redis 6+ ACL authentication ([#3071](https://github.com/DataDog/integrations-extras/pull/3071))
* Add `socket_timeout` config option to prevent the check from hanging on unreachable sentinels ([#3071](https://github.com/DataDog/integrations-extras/pull/3071))

## 1.1.1 / 2023-07-26

* [Fixed] Removed logged instance line from check ([#1183](https://github.com/DataDog/integrations-extras/pull/2059))

