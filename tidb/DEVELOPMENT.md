# Local Dev Guide (in macOS)

1. Set up the [Agent dev tool][1].

> Use `ddev` 21 or later on Python 3.13 or later. Check the installed version with `ddev --version`.

2. Install the [Datadog Agent][2].

3. Write some code.

4. Update the metadata (fields, configs, docs, etc.):

   ```shell
   ddev validate config --sync tidb
   ```

5. Reformat:

   ```shell
   ddev test -fs tidb
   ```

6. Run the tests (unit & integration):

   ```shell
   ddev test tidb
   ```

   To run only unit tests in the Python 3.13 test environment:

   ```shell
   ddev test tidb --envs py3.13 --pytest-args='-m unit -x'
   ```

7. Set up the manual test environment:

   - CD to the `./tidb/tests/compose` directory.
   - Use `docker-compose up` to start a dev TiDB cluster.
   - Build, install, and uninstall TiDB integration:
   
     ```shell
     ddev clean tidb
     ddev release build tidb
     sudo datadog-agent integration remove datadog-tidb
     sudo datadog-agent integration install -w /path/to/wheel.whl
     ```
     
     > Removing the integration does not remove `conf.d/tidb/*` at the same time. Remove it manually if necessary.

8. Conduct a manual test:

   Check local Agent log and web app carefully.

[1]: https://datadoghq.dev/integrations-core/setup/
[2]: https://docs.datadoghq.com/getting_started/agent/
