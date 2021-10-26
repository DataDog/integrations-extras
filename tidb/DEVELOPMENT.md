# Local dev guide (in macOS)

1. Set up agent dev tool

   [https://datadoghq.dev/integrations-core/setup/](https://datadoghq.dev/integrations-core/setup/)

2. Install datadog agent

   [https://docs.datadoghq.com/getting_started/agent/](https://docs.datadoghq.com/getting_started/agent/)

3. Write some code ...

4. Update metadata (fields, configs, docs, etc.)

   ```shell
   ddev validate config --sync tidb
   ```

5. Reformat

   ```shell
   ddev test -fs tidb
   ```

6. Tests (unit & integration)

   ```shell
   ddev test tidb
   ```

7. Set up manual test env

   - Use `tiup playground --monitor=0` to start a dev TiDB cluster
   - Build & install & uninstall TiDB integration
     ```shell
     ddev release build tidb
     sudo datadog-agent integration install -w /path/to/wheel.whl
     sudo datadog-agent integration remove datadog-tidb
     ```
     > Removing integration will not remove `conf.d/tidb/*` at the same time. You should remove it manually if necessary.

8. Manual test

   Check local agent log and web app carefully.
