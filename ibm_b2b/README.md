# IBM Sterling Connect:Direct Integration

## Overview

IBM Sterling Connect:Direct is a managed file transfer solution used to move files reliably between systems. The Datadog IBM Sterling Connect:Direct integration monitors process activity through the IBM Connect:Direct Web Services REST API.

The check establishes an authenticated session with Connect:Direct Web Services and reads existing process statistics. It does not submit, start, stop, or delete processes, or change Connect:Direct configuration, so it does not interfere with file transfers.

The integration reports process counts, transfer bytes, Connect:Direct Web Services connectivity, and statistics collection availability.

## Setup

### Prerequisites

- IBM Sterling Connect:Direct with IBM Connect:Direct Web Services enabled.
- Connect:Direct Web Services reachable from the Datadog Agent over HTTPS.
- A Connect:Direct Web Services user permitted to authenticate and query statistics.
- The Datadog Agent installed on a host with network connectivity to the Web Services endpoint.

### Installation

The integration is intended to run with the Datadog Agent. Install the `ibm_b2b` integration package if it is not bundled with your Agent build.

### Configuration

Create `ibm_b2b.d/conf.yaml` in the Agent `conf.d` directory:

```yaml
init_config:

instances:
  - url: https://connect-direct.example.com:1368
    username: datadog-monitor
    password: "<PASSWORD>"
    cd_node: connect-direct-node
    cd_port: 1363
    cd_protocol: TCPIP
    tls_verify: true
    timeout: 10
    statistics_timezone: America/Chicago
    statistics_lookback_minutes: 2
    min_collection_interval: 60
```

Use your secret management process to provide `password`. Do not store a real password in a shared configuration file.

| Option | Required | Description |
| --- | --- | --- |
| `url` | Yes | Base URL for IBM Connect:Direct Web Services. |
| `username` | Yes | User name used to authenticate with Web Services. |
| `password` | Yes | Password used to authenticate with Web Services. |
| `cd_node` | Yes | Host name or IP address of the Connect:Direct node to sign on to. |
| `cd_port` | No | Connect:Direct node port. Defaults to `1363`. |
| `cd_protocol` | No | Protocol used to connect to the node. Defaults to `TCPIP`. |
| `tls_verify` | No | Whether to verify the Web Services TLS certificate. Defaults to `true`. |
| `timeout` | No | HTTP request timeout in seconds. Defaults to `10`. |
| `statistics_timezone` | Required for statistics | IANA timezone of the Connect:Direct server/node, used to calculate statistics query times. For example, `America/Chicago`. Set this to the server's timezone; do not assume it matches the Agent's timezone. |
| `statistics_lookback_minutes` | No | How far back to query statistics on each run. Defaults to `2` minutes. The overlapping lookback window helps reduce the risk of missing records between runs. |
| `min_collection_interval` | No | Datadog Agent check interval in seconds. |

The check signs on at `/cdwebconsole/svc/signon` and queries existing statistics at `/cdwebconsole/svc/selectstatistics`.

## Data Collected

### Metrics

| Metric | Description |
| --- | --- |
| `ibm_b2b.processes.total` | Number of distinct processes found in the queried statistics. |
| `ibm_b2b.processes.success` | Number of processes whose statistics records have condition code zero. |
| `ibm_b2b.processes.failed` | Number of processes with at least one nonzero condition code. |
| `ibm_b2b.transfer.bytes_sent` | Bytes sent reported by transfer statistics. |
| `ibm_b2b.transfer.bytes_received` | Bytes received reported by transfer statistics. |

Metrics are tagged with `process_name` and `secondary_node` when those values are available in the statistics response.

### Service Checks

- `ibm_b2b.can_connect`: `OK` when sign-on to Connect:Direct Web Services succeeds; otherwise `CRITICAL`.
- `ibm_b2b.statistics.can_collect`: `OK` when statistics are queried and processed successfully; otherwise `CRITICAL`.

### Events

This integration does not emit events.

## Troubleshooting

- Confirm the `url` is the base URL of Connect:Direct Web Services and is reachable from the Agent.
- Verify the configured user can authenticate and query statistics, and that `cd_node`, `cd_port`, and `cd_protocol` identify the intended node.
- Confirm `statistics_timezone` is a valid IANA timezone for the Connect:Direct server/node.
- Check Agent logs and the service check messages for sign-on or statistics collection failures. Confirm certificate trust when `tls_verify` is enabled.

## Support

If you need help, contact Datadog Support.
