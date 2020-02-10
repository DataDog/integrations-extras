# Agent Check: win_docker_daemon

## Overview

This check monitors [win_docker_daemon][1] through the Datadog Agent.  This integration targets gathering docker stats from the daemon api for Windows containers.  The core docker integration uses the filesystem\cgroups to gather performance stats.  This approach does not work with Windows.  This integration attempts to create the same metrics as the docker integration.  It currently targets:
- events
- cpu
- memory
- network

This module borrows heavily from the old docker_daemon plugin.

### Installation

To install the win_docker_daemon check on your host:

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit) on any machine.
2. Run `ddev release build win_docker_daemon` to build the package.
3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).
4. Upload the build artifact to any host with an Agent andrun `datadog-agent integration install -w path/to/win_docker_daemon/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `win_docker_daemon.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your win_docker_daemon performance data. See the [sample win_docker_daemon.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `win_docker_daemon` under the Checks section.

## Data Collected

### Metrics
| name | type  | description |
|------|-------|-------------|
| docker.containers.stopped         | gauge |   |
| docker.containers.stopped.total   | gauge |   |
| docker.containers.running         | gauge |   |
| docker.containers.running.total   | gauge |   |
| docker.cpu.usage                  | gauge |   |
| docker.cpu.usage.95percentile     | gauge | 95th percentile of docker.cpu.usage|
| docker.cpu.usage.avg              | gauge | Average value of docker.cpu.usage|
| docker.cpu.usage.count            | rate  | The rate that the value of docker.cpu.usage was sampled|
| docker.cpu.usage.max              | gauge | Max value of docker.cpu.usage |
| docker.cpu.usage.median           | gauge | Median value of docker.cpu.usage|
| docker.cpu.system                 | gauge |
| docker.cpu.system.95percentile    | gauge | 95th percentile of docker.cpu.system
| docker.cpu.system.avg             | gauge | Average value of docker.cpu.system
| docker.cpu.system.count           | rate  | The rate that the value of docker.cpu.system was sampled
| docker.cpu.system.max             | gauge | Max value of docker.cpu.system
| docker.cpu.system.median          | gauge |
| docker.cpu.user                   | gauge |
| docker.cpu.user.95percentile      | gauge | 95th percentile of docker.cpu.user
| docker.cpu.user.avg               | gauge | Average value of docker.cpu.user
| docker.cpu.user.count             | rate  | The rate that the value of docker.cpu.user was sampled
| docker.cpu.user.max               | gauge | Max value of docker.cpu.user
| docker.cpu.user.median            | gauge | Median value of docker.cpu.user
| docker.mem.commit                 | gauge |
| docker.mem.commit.95percentile    | gauge | 95th percentile of docker.mem.commit
| docker.mem.commit.avg             | gauge | Average value of docker.mem.commit
| docker.mem.commit.count           | rate  | The rate that the value of docker.mem.commit was sampled
| docker.mem.commit.max             | gauge | Max value of docker.mem.commit
| docker.mem.commit.median          | gauge | Median value of docker.mem.commit
| docker.mem.rss'                   | gauge |
| docker.mem.rss.95percentile       | gauge | 95th percentile of docker.mem.ws
| docker.mem.rss.avg                | gauge | Average value of docker.mem.ws
| docker.mem.rss.count              | rate  | The rate that the value of docker.mem.ws was sampled
| docker.mem.rss.max                | gauge | Max value of docker.mem.ws
| docker.mem.rss.median             | gauge | Median value of docker.mem.ws
| docker.net.bytes_rcvd'            | rate  | Byte rate being received 
| docker.net.bytes_sent             | rate | Byte rate being sent


### Service Checks
- docker.exit


### Events
- Die
- Create
- Start


## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://github.com/DataDog/integrations-core/blob/master/win_docker_daemon/datadog_checks/win_docker_daemon/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[6]: https://docs.datadoghq.com/help


### TODO's
- [X] unit tests
- [ ] integration tests