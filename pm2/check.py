# (C) Datadog, Inc. 2015-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import subprocess
import json
import time

from checks import AgentCheck


def load_json(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    out = p.communicate()[0]
    return json.loads(out)


class Pm2(AgentCheck):

    def check(self, instance):

        for i in load_json(i['command'].split(' ')):
            node_app_instance = i['pm2_env']['NODE_APP_INSTANCE']

            tags = ["node_id:%s" % node_app_instance]

            # cpu, memory, errors, processes, restart
            self.gauge('pm2.processes.cpu'.format(node_app_instance), i['monit']['cpu'], tags=tags)
            self.gauge('pm2.processes.memory'.format(node_app_instance), i['monit']['memory'], tags=tags)
            self.gauge('pm2.processes.restart'.format(node_app_instance), i['pm2_env']['restart_time'], tags=tags)


        self.gauge('pm2.processes.processes', instance['pm2_env']['instances'])
