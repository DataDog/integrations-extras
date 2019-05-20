**Docker Windows Agent Check**
> Information: 

This custom agent check will connect to the Datadog agent running on your local Windows host to connect to your Windows Docker containers. Once connected this check will collect health based metrics around the Windows containers that are running and report the data to your Datadog instance. 

> Setup:

Within your Windows computer you must have the Datadog agent installed, (version 6+). More information about this can be found, [here.](https://docs.datadoghq.com/agent/basic_agent_usage/windows/?tab=agentv6)

Once the Datadog agent has been installed onto your Windows computer, the next thing that you will want to do is navigate to: `C:\ProgramData\Datadog`. Within the `/checks.d` copy and past the `win_docker.py` file, (which can be found within this repo).

Next, navigate to the `/conf.d` directory and create a new folder called `win_docker.d`. Within the `/conf.d/win_docker.d` directory copy & paste the `conf.yaml` file, (which can be found in this repo).

Finally, you will need to restart your Datadog agnet and within a few moments the newly discovered Windows Docker container metrics will begin to report into Datadog. 