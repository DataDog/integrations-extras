import os
import re
from collections import defaultdict

from datadog_checks.base.checks import NetworkCheck, Status
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

EVENT_TYPE = SOURCE_TYPE_NAME = 'snmpwalk'


class BinaryUnavailable(Exception):
    pass


class SnmpwalkCheck(NetworkCheck):
    """
    This is a work-alike for checks.d/snmp.py that makes use of snmpwalk for
    performance reasons. It's much faster than making the calls directly with
    pysnmp in our use-cases. It is not a 100% reimplementation. It only supports
    the functionality that we currently use. Other differences include:
        * regex matching for dynamic tagging w/additional_tags
        * tags using "enum" values emit the human-readable form instead of the
          integer.
    """

    DEFAULT_SNMPWALK_PATH = '/usr/bin/snmpwalk'
    DEFAULT_RETRIES = 2
    DEFAULT_TIMEOUT = 1
    COUNTER_TYPES = frozenset(('Counter32', 'Counter64', 'ZeroBasedCounter64'))
    GAUGE_TYPES = frozenset(('Gauge32', 'Unsigned32', 'CounterBasedGauge64', 'INTEGER', 'Integer32'))
    SC_NAME = '{}.can_check'.format(SOURCE_TYPE_NAME)

    # regex for parsing the output of snmp walk
    output_re = re.compile(r'([\w\-]+)::(?P<symbol>\w+)\.(?P<index>\d+) = ' r'(?P<type>\w+): (?P<value>.*)$')

    def __init__(self, name, init_config, agentConfig, instances=None):
        self.binary = None
        self.expected_bin = init_config.get('binary', self.DEFAULT_SNMPWALK_PATH)
        if os.path.isfile(self.expected_bin):
            self.binary = self.expected_bin

        self.mib_dirs = init_config.get('mibs_folder')

        if instances is not None:
            for instance in instances:
                # if we don't have a name add one, but mark skip_event so that we
                # don't emit the event
                if 'name' not in instance:
                    instance['name'] = self._get_instance_addr(instance)
                instance['skip_event'] = True

        NetworkCheck.__init__(self, name, init_config, agentConfig, instances)

    def _get_instance_addr(self, instance):
        host = instance.get('host', None)
        ip = instance.get('ip_address', None)
        port = instance.get('port', None)
        if host and port:
            key = "{host}:{port}".format(host=host, port=port)
        elif ip and port:
            key = "{host}:{port}".format(host=ip, port=port)
        elif host:
            key = host
        elif ip:
            key = ip

        return key

    def _check(self, instance):
        if not self.binary:
            raise BinaryUnavailable("Cannot find executable: {}".format(self.expected_bin))

        ip_address = self._get_instance_addr(instance)
        metrics = instance.get('metrics', [])
        community_string = instance.get('community_string', 'public')
        timeout = int(instance.get('timeout', self.DEFAULT_TIMEOUT))
        retries = int(instance.get('retries', self.DEFAULT_RETRIES))

        hostname = instance.get('metric_host', None)

        # Build up our dataset
        data = defaultdict(dict)
        types = {}
        for metric in metrics:
            mib = metric['MIB']
            table = metric['table']
            cmd = [self.binary, '-c{}'.format(community_string), '-v2c', '-t', str(timeout), '-r', str(retries)]
            if self.mib_dirs:
                cmd.extend(['-M', self.mib_dirs])
            cmd.extend([ip_address, '{}:{}'.format(mib, table)])

            try:
                output = get_subprocess_output(cmd, self.log)[0]
            except Exception as e:
                error = "Fail to collect metrics for {0} - {1}".format(instance['name'], e)
                self.log.warning(error)
                return [(self.SC_NAME, Status.CRITICAL, error)]

            for line in output.splitlines():
                if not line:
                    continue
                match = self.output_re.match(line)
                if match is not None:
                    symbol = match.group('symbol')
                    index = int(match.group('index'))
                    value = match.group('value')
                    typ = match.group('type')
                    types[symbol] = typ
                    if typ == 'INTEGER':
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                    elif value == '':
                        value = None
                    data[symbol][index] = value
                else:
                    # TODO: remove this
                    self.log.warning('Problem parsing output of snmp walk: %s', line)

        # Get any base configured tags and add our primary tag
        tags = instance.get('tags', []) + ['snmp_device:{}'.format(ip_address)]

        # It seems kind of weird, but from what I can tell the snmp check allows
        # you to add symbols to a metric that were retrieved by another metric,
        # both for values and tags. So you can add a symbol in the 1st metric
        # that pulls data from the 2nd. Same applies to tag lookups. Seems like
        # symbols should have been at the instance level rather than
        # per-metric... That way the bahavior would match up with schema, but oh
        # well.

        # Time to emit metrics
        for metric in metrics:

            # Build a list of dynamic tags per-index
            dynamic_tags = defaultdict(list)
            for metric_tag in metric.get('metric_tags', []):
                if 'column' in metric_tag:
                    tag = metric_tag['tag']
                    column = metric_tag['column']
                    regex = metric_tag.get('regex', None)
                    if regex is not None:
                        # pre-compile our regex
                        regex = re.compile(regex)
                    for i, v in data[column].items():
                        if v is None:
                            # No value for the column, ignore
                            continue
                        elif types[column] == 'INTEGER':
                            # enum/bool etc, use the human readable name
                            v = v.split('(')[0]

                        if regex is not None:
                            # There's a regex for this tag
                            match = regex.match(v)
                            if match is not None:
                                # It matches so we'll apply it, group(1) becomes
                                # the value
                                v = match.group(1)
                                dynamic_tags[i].append('{}:{}'.format(tag, v))
                                additional_tags = metric_tag.get('additional_tags', [])
                                # and we add any additional tags
                                dynamic_tags[i].extend(additional_tags)
                        else:
                            # This is a standard tag, just use the value
                            dynamic_tags[i].append('{}:{}'.format(tag, v))
                else:
                    self.log.debug('unsupported metric_tag: %s', metric_tag)
                    continue

            symbols = metric.get('symbols', [])
            # For each of the symbols we'll be recording as a metric
            for symbol in symbols:
                # For each value for that symbol
                for i, value in data[symbol].items():
                    if value is None:
                        # skip empty
                        continue
                    # metric key
                    key = '{}.{}'.format(SOURCE_TYPE_NAME, symbol)
                    value = int(value)

                    typ = types[symbol]
                    if typ in self.COUNTER_TYPES:
                        self.rate(key, value, tags + dynamic_tags[i], hostname=hostname)
                    elif typ in self.GAUGE_TYPES:
                        self.gauge(key, value, tags + dynamic_tags[i], hostname=hostname)
                    else:
                        raise Exception('unsupported metric symbol type: {}'.format(typ))

        return [(self.SC_NAME, Status.UP, None)]

    def report_as_service_check(self, sc_name, status, instance, msg=None):
        sc_tags = ['snmp_device:{0}'.format(instance['name'])]
        custom_tags = instance.get('tags', [])
        tags = sc_tags + custom_tags

        self.log.debug('Submitting with the following tags: %s', sc_tags)
        self.service_check(sc_name, NetworkCheck.STATUS_TO_SERVICE_CHECK[status], tags=tags, message=msg)
