
from typing import Any

try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck, ConfigurationError
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

from datadog_checks.base.log import DEFAULT_FALLBACK_LOGGER, get_check_logger, init_logging

import requests

# Some basics
__version__ = "1.0.0"
__metric_base__ = "voltdb"

# Reserved tag fields
RESERVED_TAG_WORDS = ["HOST_ID", "SITE_ID", "PARTITION_ID", "CLUSTER_ID", "REMOTE_CLUSTER_ID"]

# VoltDB reported "types"... idk, but this seems arbitrary...
STRING = 9
BIGINT = 6
INT = 5
BOOL = 3

CAPTURE_PROCS = [
    "CPU", 
    "DRCONSUMER", 
    "DRPRODUCER", 
    "DRROLE", 
    "EXPORT", 
    "GC", 
    "IDLETIME", 
    "IMPORT", 
    "INDEX", 
    "INITIATOR", 
    "IOSTATS", 
    "LATENCY", 
    "LIVECLIENTS", 
    "MEMORY", 
    "PARTITIONCOUNT", 
    "PLANNER", 
    "PROCEDUREDETAIL", 
    "PROCEDUREINPUT", 
    "PROCEDUREOUTPUT",
    "PROCEDUREPROFILE",
    "QUEUE",
    "REBALANCE",
    "SNAPSHOTSTATUS",
    "TABLE",
    "TASK",
    "TTL"
]

# The actual VoltDB check
class VoltDBCheck(AgentCheck):
    def __init__(self, *args, **kwargs):
        super(VoltDBCheck, self).__init__(*args, **kwargs)
        self.log = get_check_logger()

    # Build a pretty URL
    def getURL(self, url, port, username, password, procedure, parameters):
        vdbURL = "http://%s:%d/api/1.0/?Procedure=%s&Parameters=%s&admin=false&User=%s&Password=%s" % (url, port, procedure, parameters, username, password)
        return vdbURL

    # Build metrics from data
    def buildMetrics(self, raw, prefix):
        results = raw['results'][0]
        schema = results['schema']
        data = results['data']

        tags = []
        metrics = []
        processed = []

        for i in range(len(schema)):
            if schema[i]['type'] == STRING or schema[i]['name'] in RESERVED_TAG_WORDS:
                tags.append({"index": i, "name": str(schema[i]['name']).lower()})
            else:
                if schema[i]['name'] != 'TIMESTAMP':
                    metrics.append({"index": i, "name": str(__metric_base__ + '.'+prefix+'.'+schema[i]['name'].lower())})

        # Timestamp should ****ALWAYS**** BE at 0
        for point in data:
            for m in metrics:
                newMetric = {
                    "name": m['name'],
                    "value": m['index'],
                    "tags": [],
                    "timestamp": point[0]
                    }
                for t in tags:
                    newMetric['tags'].append(str(t['name'])+':'+str(point[t['index']]))
                processed.append(newMetric)
        return processed

    # Submit actual metrics
    def submitMetrics(self, metrics):
        for m in metrics:
            self.gauge(m['name'], m['value'], tags=m['tags'])

    def captureData(self, url, port, username, password, table, procedure, namespace):
        # get url and build data
        results = requests.get(self.getURL(url, port, username, password, table, procedure))
        results.raise_for_status()
        data = results.json()
        metrics = self.buildMetrics(data, namespace)
        self.submitMetrics(metrics)
        return

    # Do CPU Checking
    def submitCPU(self, url, port, username, password):
        # get url and build data
        results = requests.get(self.getURL(url, port, username, password, '@Statistics', '["CPU"]'))
        results.raise_for_status()
        data = results.json()
        metrics = self.buildMetrics(data, "cpu")
        self.submitMetrics(metrics)
        return

    # Do the Datadog check!
    def check(self, instance):
        # Grab the config variables
        url = instance.get('url')
        port = instance.get('port')
        username = instance.get('username')
        password = instance.get('password')

        # Check configuration for integration
        if not url or not port or not username or not password:
            raise ConfigurationError('There is a configuration error, please fix conf.yaml in voltdb.d!')

        # Run the cpu check...
        for proc in CAPTURE_PROCS:
            try: 
                self.captureData(url, port, username, password, "@Statistics", '["'+proc+'"]', str(proc).lower())
            except Exception as e:
                raise ConfigurationError('There is a collection error for voltdb.d for: '+proc+'!')
