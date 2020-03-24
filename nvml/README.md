# Agent Check: nvml

## Overview

This check monitors [nvidia nvml][1] exposed metrics through the Datadog Agent and can correlate them
with the [exposed kuberneties devices][8].

## Setup

This package is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `nvml` package, run:

   ```shell
   ddev -e release build nvml
   ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_NVML_ARTIFACT_>/<NVML_ARTIFACT_NAME>.whl
   # You may also need to install dependencies since those aren't packaged into the wheel (I'm not sure why)
   sudo -u dd-agent -H /opt/datadog-agent/embedded/bin/pip3 install grpcio pynvml
   ```

If you are using Docker, there is an example Dockerfile in the nvml repository.

   ```shell
   docker build --build-arg=DD_AGENT_VERSION=7.18.0 .
   ```

7. Configure your integration like [any other packaged integration][7].

8. If you're using Docker and k8s, you will need to expose the environment variables NVIDIA_VISIBLE_DEVICES and NVIDIA_DRIVER_CAPABILITIES.  See the included Dockerfile for an example.

9. If you want to be able to correlate reserved k8s nvidia devices with the k8s pod using the device, you will need to mount the Unix domain socket `/var/lib/kubelet/pod-resources/kubelet.sock` into your agent's configuration.  More
information about this socket is on the kubernetes [website][8].  Note this device is in beta support for version 1.15.

### Configuration

1. Edit the `nvml.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your nvml performance data. See the [sample nvml.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `nvml` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.  The authoritative metric documentation is on the [nvidia website][9].

There is an attempt to, when possible, match metric names with Nvidia's [dcgm exporter][10].

### Service Checks

nvml does not include any service checks.

### Events

nvml does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://pypi.org/project/pynvml/
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://github.com/DataDog/integrations-core/blob/master/nvml/datadog_checks/nvml/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-core/blob/master/nvml/metadata.csv
[7]: https://docs.datadoghq.com/help
[8]: https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources
[9]: https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html
[10]:https://github.com/NVIDIA/gpu-monitoring-tools/blob/master/exporters/prometheus-dcgm/dcgm-exporter/dcgm-exporter
