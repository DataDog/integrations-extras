# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import platform

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

from .net_api import vManageApi


class NnSdwanCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'nn_sdwan'

    def __init__(self, name, init_config, instances):
        super(NnSdwanCheck, self).__init__(name, init_config, instances)

        # Validate instance config fields are present
        for field in 'hostname username password protocol'.split():
            if not self.instance.get(field):
                raise ConfigurationError(f'Configuration error: "{field}" not present.')

        self.vmanage_api = vManageApi(instance=instances[0])

    def check(self, _):
        # Handle service check (availablity / reachability)
        if not self.pingable(self.instance.get('hostname')):
            self.service_check('nn_sdwan.sdwan_controller.online', self.CRITICAL, message='Host unreachable.')
            return

        try:
            self.vmanage_api.get_device_info()
            # vManage is online and responding
            self.service_check('nn_sdwan.sdwan_controller.online', self.OK)
        except Exception:
            self.service_check(
                'nn_sdwan.sdwan_controller.online', self.WARNING, message='vManage API is not responding.'
            )
            return

        # Get metrics
        for method in (
            self.get_control_status,
            self.get_top_application_stats,
            self.get_application_aware_routing,
            self.get_connection_summary_stats,
            self.get_certificate_summary,
            self.get_reboot_count,
            self.get_vmanage_count,
            self.get_site_health,
            self.get_transport_interface,
            self.get_wan_edge_health,
            self.get_wan_edge_inventory,
        ):
            try:
                method()
            except Exception as e:
                self.log.exception(e)

    def pingable(self, host: str):
        """
        Returns True if host (str) responds to a ping request.
        """

        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        out, err, retcode = get_subprocess_output(command, self.log, raise_on_empty_output=False)
        return retcode == 0

    def get_wan_edge_inventory(self):
        wan_edge_inven_stats = self.vmanage_api.get_wan_edge_inventory().get('data')
        if wan_edge_inven_stats is None:
            return
        for result in wan_edge_inven_stats:
            self.gauge(name='wan_edge_inventory', tags=[f'name:{result["name"]}'], value=result['value'])

    def get_wan_edge_health(self):
        wan_edge_health_stats = self.vmanage_api.get_wan_edge_health().get('data')
        if wan_edge_health_stats is None:
            return
        for result in wan_edge_health_stats:
            self.gauge(name='wan_edge_health', tags=[f'status:{result["status"]}'], value=result['count'])

    def get_transport_interface(self):
        transport_int_stats = self.vmanage_api.get_transport_interface().get('data')
        if transport_int_stats is None:
            return
        for result in transport_int_stats:
            self.gauge(
                name='transport_interface',
                tags=[f'percentageDistribution:{result["percentageDistribution"]}'],
                value=result['value'],
            )

    def get_site_health(self):
        site_health_stats = self.vmanage_api.get_site_health().get('data')
        if site_health_stats is None:
            return
        for result in site_health_stats:
            self.gauge(name='site_health', tags=[f'status:{result["status"]}'], value=result['count'])

    def get_vmanage_count(self):
        vmanage_count_stats = self.vmanage_api.get_vmanage_count()
        if len(vmanage_count_stats.keys()) == 0:
            return
        self.gauge(name='vmanage_count', tags=['status:total'], value=vmanage_count_stats['count'])
        for result in vmanage_count_stats['statusList']:
            self.gauge(name='vmanage_count', tags=[f'status:{result["status"]}'], value=result['count'])

    def get_reboot_count(self):
        reboot_stats = self.vmanage_api.get_reboot_count()
        if len(reboot_stats.keys()) == 0:
            return
        self.gauge(name='reboot_count', tags=[], value=reboot_stats["count"])

    def get_certificate_summary(self):
        cert_summary_stats = self.vmanage_api.get_certificate_summary()
        if len(cert_summary_stats.keys()) == 0:
            return
        self.gauge(name='cert_summary', tags=['status:invalid'], value=cert_summary_stats["invalid"])
        self.gauge(name='cert_summary', tags=['status:warning'], value=cert_summary_stats["warning"])

    def get_connection_summary_stats(self):
        conn_summary_stats = self.vmanage_api.get_connection_summary().get('connection_summary')
        if conn_summary_stats is None or len(conn_summary_stats) == 0:
            return
        for result in conn_summary_stats:
            tags = [f'device:{result["device"]}']
            self.gauge(name='connection_summary_stats_error', tags=tags, value=result["error"])
            self.gauge(name='connection_summary_stats_total', tags=tags, value=result["total"])

    def get_control_status(self):
        control_status_stats = self.vmanage_api.get_control_status().get('data')
        if control_status_stats is None:
            return
        points = [(report['count'], {'name': report['name']}) for report in control_status_stats]
        for point in points:
            tags = [f'{key}:{val}' for (key, val) in point[1].items()]
            self.gauge(name='device_control_status', value=point[0], tags=tags)

    def get_top_application_stats(self):
        top_application_stats = self.vmanage_api.get_top_application().get('data')
        if top_application_stats is None:
            return
        for result in top_application_stats:
            tags = [f'application:{result["application"]}']
            self.gauge(name='top_app_stats', value=result['octets'], tags=tags)

    def get_application_aware_routing(self):
        metric = 'app_aware_routing'
        app_aware_routing_stats = self.vmanage_api.get_app_aware_routing().get('data')
        if app_aware_routing_stats is None:
            return
        for result in app_aware_routing_stats:
            tags = [f'name:{result["name"]}']
            for metric_name in 'jitter latency loss_percentage rx_octets tx_octets'.split():
                self.gauge(
                    name=f'{metric}.{metric_name}',
                    value=result[metric_name],
                    tags=tags,
                )
