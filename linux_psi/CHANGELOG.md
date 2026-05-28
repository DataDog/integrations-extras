# CHANGELOG - Linux PSI

All notable changes to this integration are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0 / 2026-05-28

### Added

- Initial release of the `linux_psi` integration.
- Reads `/proc/pressure/{cpu,memory,io}` and emits 24 metrics covering the
  `some`/`full` x `avg10`/`avg60`/`avg300`/`total` matrix for each resource.
- `linux_psi.can_read` service check with WARNING when PSI is not enabled
  on the kernel and CRITICAL on permission errors.
- Three recommended monitors: high CPU pressure, severe memory pressure, high
  I/O pressure.
- Overview dashboard with timeseries panels for the three resources and top
  lists for the busiest hosts.
- Honors the Agent's `procfs_path` config for containerized deployments that
  mount the host's `/proc` at `/host/proc`.
- Graceful handling of kernels older than 5.13 that lack the `full` line for
  `/proc/pressure/cpu`.
