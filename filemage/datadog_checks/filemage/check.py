import csv
import os
from urllib.parse import urljoin

import psutil
import requests

from datadog_checks.base import AgentCheck, ConfigurationError

from .common import FTP_METRIC_PREFIX, NAMESPACE


# define our custom version to avoid dependency hell
def get_metadata_metrics():
    metadata_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata.csv')
    with open(metadata_path) as f:
        return {row['metric_name']: row for row in csv.DictReader(f)}


class FilemageCheck(AgentCheck):
    # this will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = NAMESPACE
    # the FTP commands that will be tracked via metric submissions
    TRACKED_METRICS_META = get_metadata_metrics()
    FTP_TRACKED_METRICS = TRACKED_METRICS_META.keys()
    FTP_TRACKED_CMDS = [metric.replace(f'{NAMESPACE}.{FTP_METRIC_PREFIX}.', '') for metric in FTP_TRACKED_METRICS]
    FTP_STATS_BASE = {x: 0.0 for x in FTP_TRACKED_CMDS}

    def __init__(self, name, init_config, instances):
        super(FilemageCheck, self).__init__(name, init_config, instances)

        # validate instance configs
        self.filemage_service_checks = self.instance.get('filemage_service_checks')
        if self.filemage_service_checks is None:
            raise ConfigurationError('Instance Misconfiguration: filemage_service_checks is not valid')
        self.filemage_api_config = self.instance.get("filemage_api_config")
        if self.filemage_api_config is None:
            raise ConfigurationError('Instance Misconfiguration: filemage_api_config is not valid')

    def check(self, _):
        """
        Run the filemage service checks and send metrics to datadog API
        """

        # check if filemage processes are alive
        down_services = []
        for service in self.filemage_service_checks:
            if not FilemageCheck.isProcAlive(service):
                down_services.append(service)
        if len(down_services) != 0:
            self.service_check(
                "services_up", AgentCheck.CRITICAL, message=f'the following filemage services are down: {down_services}'
            )
            self.log.warning('the following filemage services are down: %s', repr(down_services))
            return

        self.service_check("services_up", AgentCheck.OK)
        self.log.debug('all filemage services are up')

        # gather and send metrics
        try:
            r = requests.get(
                urljoin(f'{self.filemage_api_config["rooturl"]}', 'logs'),
                headers={'Accept': 'application/json', 'filemage-api-token': self.filemage_api_config['apitoken']},
                verify=self.filemage_api_config['verifyssl'],
                allow_redirects=True,
            )
            r.raise_for_status()

            # get the FTP statistics
            stats = FilemageCheck.FTP_STATS_BASE.copy()
            for entry in r.json():
                if entry['operation'] not in FilemageCheck.FTP_TRACKED_CMDS:
                    self.log.warning('skipping untracked FTP entry: %s', repr(entry))
                    continue
                stats[entry['operation']] += 1

            # send the tracked statistics
            for k, v in stats.items():
                self.count(f'{FTP_METRIC_PREFIX}.{k}', v)
        except Exception as ex:
            self.service_check("metrics_up", AgentCheck.WARNING, message='could not retrieve FTP metrics from filemage')
            self.log.warning('could not retrieve FTP metrics from filemage: %s', str(ex))
            return

        self.service_check("metrics_up", AgentCheck.OK)
        self.log.debug('submitted filemage FTP metrics')

    @staticmethod
    def isProcAlive(name):
        """
        Check if a process is running.

        :param name:    Process name to check
        :type name:     str
        :return:        Whether the process is running or not
        :rtype:         bool
        """

        return any(proc.info['name'] == name for proc in psutil.process_iter(['name']))
