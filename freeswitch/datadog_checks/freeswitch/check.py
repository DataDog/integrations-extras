import json
import os
import re
import subprocess

import psutil

from datadog_checks.base import AgentCheck


class FreeswitchCheck(AgentCheck):
    # this will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'freeswitch'

    def __init__(self, name, init_config, instances):
        super(FreeswitchCheck, self).__init__(name, init_config, instances)

    def check(self, instance):
        """
        Run the freeswitch service checks and send metrics to datadog API

        :param instance:    The current instance configuration
        :type instance:     object|dict
        :return:            None
        :rtype:             None
        """

        # validate instance configs
        fs_conf_dir = instance.get('freeswitch_conf_dir')
        if fs_conf_dir is None:
            self.service_check(
                "services_up", AgentCheck.WARNING, message='agent misconfiguration: freeswitch_conf_dir is not valid'
            )
            return None

        # check if freeswitch process is alive
        if not FreeswitchCheck.isProcAlive('freeswitch'):
            self.service_check("services_up", AgentCheck.CRITICAL, message='freeswitch service is down')
            return None

        self.service_check("services_up", AgentCheck.OK, message='freeswitch service is up')

        # gather and send metrics
        try:
            fs_cli_cmd = FreeswitchCheck.getFreeswitchCliCmd(fs_conf_dir)

            p = subprocess.Popen(
                [*fs_cli_cmd, '-x', 'show bridged_calls as json'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            data = json.loads(p.communicate()[0].decode('utf-8'))
            self.gauge('bridged_calls', float(data['row_count']))

            p = subprocess.Popen(
                [*fs_cli_cmd, '-x', 'show calls as json'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            data = json.loads(p.communicate()[0].decode('utf-8'))
            self.gauge('calls', float(data['row_count']))

            p = subprocess.Popen(
                [*fs_cli_cmd, '-x', 'show channels as json'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            data = json.loads(p.communicate()[0].decode('utf-8'))
            self.gauge('channels', float(data['row_count']))

            p = subprocess.Popen(
                [*fs_cli_cmd, '-x', 'show registrations as json'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            data = json.loads(p.communicate()[0].decode('utf-8'))
            self.gauge('registrations', float(data['row_count']))

            p = subprocess.Popen(
                [*fs_cli_cmd, '-x', 'sofia jsonstatus'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            data = json.loads(p.communicate()[0].decode('utf-8'))

            regex = re.compile('^(NOREG|REGED)$')
            active_profiles = 0.0
            active_gateways = 0.0
            for k, v in data['profiles'].items():
                if v['status']['type'] != 'profile':
                    continue
                if v['status']['state'] == "RUNNING":
                    active_profiles += 1
                else:
                    self.service_check(
                        "services_up", AgentCheck.WARNING, message=f'found inactive freeswitch profile: {k}'
                    )
                if 'gateways' in v:
                    for gk, gv in v['gateways'].items():
                        if regex.match(gv['state']):
                            active_gateways += 1
                        else:
                            self.service_check(
                                "services_up", AgentCheck.WARNING, message=f'found inactive freeswitch gateway: {gk}'
                            )
            self.gauge('profiles', active_profiles)
            self.gauge('gateways', active_gateways)

        except Exception:
            self.service_check(
                "metrics_up", AgentCheck.WARNING, message='could not retrieve statistics from freeswitch'
            )
            raise
        self.service_check("metrics_up", AgentCheck.OK, message='freeswitch metrics submitted')

    @staticmethod
    def isProcAlive(name):
        """
        Check if a process is running.

        :param name:    Process name to check
        :type name:     str
        :return:        Whether the process is running or not
        :rtype:         bool
        """

        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == name:
                return True
        return False

    @staticmethod
    def getFreeswitchCliCmd(fs_conf_dir):
        fs_esl_conf = os.path.join(fs_conf_dir, 'autoload_configs', 'event_socket.conf.xml')
        with open(fs_esl_conf, 'r') as f:
            s = f.read()
            fs_esl_ip = re.search(
                r'''<param[ \t]+name=(?P<quote1>["'])listen-ip(?P=quote1)[ \t]+value=(?P<quote2>["'])(.*?)(?P=quote2)[ \t]*/>''',  # noqa: E501
                s,
            ).group(3)
            fs_esl_port = re.search(
                r'''<param[ \t]+name=(?P<quote1>["'])listen-port(?P=quote1)[ \t]+value=(?P<quote2>["'])(.*?)(?P=quote2)[ \t]*/>''',  # noqa: E501
                s,
            ).group(3)
            fs_esl_pass = re.search(
                r'''<param[ \t]+name=(?P<quote1>["'])password(?P=quote1)[ \t]+value=(?P<quote2>["'])(.*?)(?P=quote2)[ \t]*/>''',  # noqa: E501
                s,
            ).group(3)
        return ['fs_cli', f'--host={fs_esl_ip}', f'--port={fs_esl_port}', f'--password={fs_esl_pass}']
