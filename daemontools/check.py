# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import re
import subprocess

# project
from checks import AgentCheck


EVENT_TYPE = SOURCE_TYPE_NAME = 'daemontools'

DT_STATUS = re.compile(".*: (down|up) \(pid (\d+)\) (\d+) seconds")

class DaemontoolsCheck(AgentCheck):

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        path = instance.get('path', '/etc/service')
        if path is None:
            raise Exception("Must provide a path where services are installed!")
        service = instance.get('service')
        if service is None:
            raise Exception("Must provide a service to check!")
        tags = instance.get('tags', [])
        tags.append("service:" + service)

        status = subprocess.Popen(['svstat', path + "/" + service], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        check_status = AgentCheck.CRITICAL
        dt_result = DT_STATUS.match(status)
        if dt_result:
            if dt_result.group(1) == "up":
                check_status = AgentCheck.OK
                self.gauge('daemontools.service.uptime', float(dt_result.group(3)), tags)
            elif dt_result.group(1) == "down":
                check_status == AgentCheck.CRITICAL
            else:
                check_status == AgentCheck.UNKNOWN

        self.service_check(
            "daemontools.is_running",
            check_status,
            message=status,
            tags=tags
        )
