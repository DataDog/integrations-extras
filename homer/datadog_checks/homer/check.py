import psutil
import psycopg2

from datadog_checks.base import AgentCheck


class ConnNoop(object):
    def close(self):
        pass


class HomerCheck(AgentCheck):
    # this will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'homer'

    def __init__(self, name, init_config, instances):
        super(HomerCheck, self).__init__(name, init_config, instances)

    def check(self, instance):
        """
        Run the homer service checks and send metrics to datadog API

        :param instance:    The current instance configuration
        :type instance:     object|dict
        :return:            None
        :rtype:             None
        """

        # validate instance configs
        homer_service_checks = instance.get('homer_service_checks')
        if homer_service_checks is None:
            self.service_check(
                "services_up", AgentCheck.WARNING, message='agent misconfiguration: homer_service_checks is not valid'
            )
            return None
        homer_config_db = instance.get("homer_config_db")
        if homer_config_db is None:
            self.service_check(
                "metrics_up", AgentCheck.WARNING, message='agent misconfiguration: homer_config_db is not valid'
            )
            return None
        homer_data_db = instance.get("homer_data_db")
        if homer_data_db is None:
            self.service_check(
                "metrics_up", AgentCheck.WARNING, message='agent misconfiguration: homer_data_db is not valid'
            )
            return None

        # check if homer processes are alive
        down_services = []
        for service in homer_service_checks:
            if not HomerCheck.isProcAlive(service):
                down_services.append(service)
        if len(down_services) != 0:
            self.service_check(
                "services_up", AgentCheck.CRITICAL, message=f'found homer services that are down: {down_services}'
            )
            return None

        self.service_check("services_up", AgentCheck.OK, message='homer services are all up')

        # gather and send metrics
        conn1 = ConnNoop()
        conn2 = ConnNoop()
        try:
            conn1 = psycopg2.connect(
                user=homer_config_db['user'],
                password=homer_config_db['pass'],
                host=homer_config_db['host'],
                port=homer_config_db['port'],
                dbname=homer_config_db['name'],
            )
            conn2 = psycopg2.connect(
                user=homer_data_db['user'],
                password=homer_data_db['pass'],
                host=homer_data_db['host'],
                port=homer_data_db['port'],
                dbname=homer_data_db['name'],
            )
            with conn1.cursor() as cur1, conn2.cursor() as cur2:
                cur1.execute("SELECT hepid, profile FROM mapping_schema WHERE hep_alias='SIP';")
                for row in cur1:
                    cur2.execute(
                        "SELECT SUM(n_live_tup) FROM pg_stat_user_tables WHERE relname LIKE CONCAT('hep_proto', '_', %s, '_', %s, '_', TO_CHAR(CURRENT_DATE, 'YYYYMMDD'), '_%%');",  # noqa: E501
                        (row[0], row[1]),
                    )
                    stat = cur2.fetchone()[0]
                    self.gauge(f'txcount.{row[1]}', float(stat))
        except Exception as ex:
            self.service_check("metrics_up", AgentCheck.WARNING, message=f'error retrieving metrics: {str(ex)}')
            return None
        finally:
            conn1.close()
            conn2.close()

        self.service_check("metrics_up", AgentCheck.OK, message='homer metrics submitted')

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
