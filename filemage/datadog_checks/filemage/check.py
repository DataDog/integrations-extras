import psutil

from datadog_checks.base import AgentCheck


class FilemageCheck(AgentCheck):
    # this will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'filemage'

    def __init__(self, name, init_config, instances):
        super(FilemageCheck, self).__init__(name, init_config, instances)

    def check(self, instance):
        """
        Run the filemage service checks and send metrics to datadog API

        :param instance:    The current instance configuration
        :type instance:     object|dict
        :return:            None
        :rtype:             None
        """

        # validate instance configs
        filemage_service_checks = instance.get('filemage_service_checks')
        if filemage_service_checks is None:
            self.service_check(
                "services_up",
                AgentCheck.WARNING,
                message='agent misconfiguration: filemage_service_checks is not valid',
            )
            return None
        filemage_api_config = instance.get("filemage_api_config")
        if filemage_api_config is None:
            self.service_check(
                "services_up", AgentCheck.WARNING, message='agent misconfiguration: filemage_api_config is not valid'
            )
            return None

        # check if filemage processes are alive
        down_services = []
        for service in filemage_service_checks:
            if not FilemageCheck.isProcAlive(service):
                down_services.append(service)
        if len(down_services) != 0:
            self.service_check(
                "services_up", AgentCheck.CRITICAL, message=f'found filemage services that are down: {down_services}'
            )
            return None

        self.service_check("services_up", AgentCheck.OK, message='filemage services are all up')

        # gather and send metrics
        try:
            r = self.http.post(
                f'{filemage_api_config["rooturl"]}logs/',
                headers={'Accept': 'application/json', 'filemage-api-token': filemage_api_config['apitoken']},
                verify=filemage_api_config['verifyssl'],
            )
            r.raise_for_status()

            stats = {}
            for entry in r.json():
                try:
                    stats[entry['operation']] += 1
                except KeyError:
                    stats[entry['operation']] = 1.0

            for k, v in stats.items():
                self.gauge(f'ftp.{k}', v)
        except Exception:
            self.service_check("metrics_up", AgentCheck.WARNING, message='could not retrieve FTP metrics from filemage')
            return None

        self.service_check("metrics_up", AgentCheck.OK, message='filemage metrics submitted')

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
