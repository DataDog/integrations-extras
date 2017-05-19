from checks import CheckException
from checks.prometheus_check import PrometheusCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'traefik'

class Traefik(PrometheusCheck):
    """
    Collect traefik metrics from Prometheus
    """
    def __init__(self, name, init_config, agentConfig, instances=None):
        super(Traefik, self).__init__(name, init_config, agentConfig, instances)
        self.NAMESPACE = 'traefik'

        self.metrics_mapper = {
            'traefik_request_duration_seconds': 'request.duration',
            'traefik_requests_total': 'requests.total',
        }


    def check(self, instance):
        endpoint = instance.get('prometheus_endpoint')
        if endpoint is None:
            raise CheckException("Unable to find prometheus_endpoint in config file.")

        send_buckets = instance.get('send_histograms_buckets', True)
        # By default we send the buckets.
        if send_buckets is not None and str(send_buckets).lower() == 'false':
            send_buckets = False
        else:
            send_buckets = True

        self.process(endpoint, send_histograms_buckets=send_buckets, instance=instance)
