# Local dev guide (in macOS)

1. Set up

[https://datadoghq.dev/integrations-core/setup/](https://datadoghq.dev/integrations-core/setup/)

2. Update metadata (fields, config, doc, etc.)

```shell
ddev validate config --sync tidb
```

4. Reformat

```shell
ddev test -fs tidb
```

5. Tests (unit & integration)

```shell
ddev test -fs tidb
```

7. Build & install & uninstall 

```shell
ddev release build tidb
sudo datadog-agent integration install -w /path/to/wheel.whl
sudo datadog-agent integration remove datadog-tidb
```

Removing integration will not delete `conf.d/tidb/*` at the same time. You should remove ti manually if necessary.

