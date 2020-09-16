import os
import re

from datadog_checks.base import AgentCheck, ConfigurationError, is_affirmative
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

EVENT_TYPE = 'unbound'


class UnboundCheck(AgentCheck):
    # Stats info https://unbound.net/documentation/unbound-control.html

    SERVICE_CHECK_NAME = 'unbound.can_get_stats'

    def check(self, instance):

        use_sudo = is_affirmative(instance.get('use_sudo', False))
        unbound_control = instance.get('unbound_control', 'unbound-control')
        stats_command = instance.get('stats_command', 'stats')
        host = instance.get('host')
        config_file = instance.get('config_file')
        tags = instance.get('tags', [])

        command = []
        if use_sudo:
            test_sudo = os.system('setsid sudo -l < /dev/null')
            if test_sudo != 0:
                raise Exception('The dd-agent user does not have sudo access')
            command.append('sudo')

        if not which(unbound_control, use_sudo, self.log):
            raise ConfigurationError('executable not found: {}'.format(unbound_control))

        command.extend((unbound_control, stats_command))
        if host:
            command.extend(('-s', host))
        if config_file:
            command.extend(('-c', config_file))

        # Call unbound-control in a separate method to facilitate mocking during testing.
        # Without this, it's difficult to mock the multiple get_subprocess_output calls
        # independently.
        ub_out = self.call_unbound_control(command, tags)

        # Example of unbound stats outpout:
        # total.num.queries=12
        # mem.cache.rrset=0
        # num.query.type.A=4
        # unwanted.queries=3

        # [(u'thread0.num.queries', u'12'), (u'thread0.num.queries_ip_ratelimited', u'45')...]
        data = re.findall(r'(\S+)=(.*\d)', ub_out)

        if not data:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message="unable to parse stats", tags=tags)
            raise Exception("unable to parse output '{}'".format(ub_out))

        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=tags)

        for stat in data:
            self.log.debug('processing %s', stat)

            # Some metric names from unbound make more sense to record as name + tag in datadog.
            metric_name, all_tags = self.metric_name_to_tags(stat[0], tags)

            unbound_metric_name = 'unbound.{}'.format(metric_name)

            if 'histogram' in metric_name:  # dont send histogram metrics
                self.log.debug('unbound.%s:%s', unbound_metric_name, stat[1])
            else:
                if any(count in metric_name for count in ['num.', 'unwanted', '.count']):
                    self.log.debug('count: %s', stat)
                    self.count(unbound_metric_name, stat[1], tags=all_tags)
                elif 'time.' in metric_name:
                    self.log.debug('gauge (time): %s', stat)
                    self.gauge(unbound_metric_name, float(stat[1]), tags=all_tags)
                else:
                    self.log.debug('gauge: %s', stat)
                    self.gauge(unbound_metric_name, float(stat[1]), tags=all_tags)

    def call_unbound_control(self, command, tags):
        try:
            # Pass raise_on_empty_output as False so we get a chance to log stderr
            ub_out, ub_err, returncode = get_subprocess_output(command, self.log, raise_on_empty_output=False)
        except Exception as e:
            self.service_check(
                self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message="exception collecting stats", tags=tags
            )
            raise Exception("Unable to get unbound stats: {}".format(str(e)))

        for line in ub_err.splitlines():
            self.log.debug('stderr from %s: %s', command, line)

        # Check the return value
        if returncode != 0:
            self.service_check(
                self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message="non-zero return code collecting stats", tags=tags
            )
            raise Exception('"{}" failed, return code: {}'.format(command, returncode))

        # And because we pass raise_on_empty_output as False, check that too
        if not ub_out:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message="no stats", tags=tags)
            raise Exception('no output from "{}"'.format(command))

        return ub_out

    def tag_handler(self, metric_name):
        TAG_HANDLERS = {
            'thread': self.thread_handler,
            'num.query.type': self.query_type_handler,
            'num.query.class': self.query_class_handler,
            'num.query.opcode': self.query_opcode_handler,
            'num.query.flags': self.query_flags_handler,
            'num.answer.rcode': self.answer_rcode_handler,
        }

        handlers = [TAG_HANDLERS[prefix] for prefix in TAG_HANDLERS.keys() if metric_name.startswith(prefix)]
        num_handlers = len(handlers)
        if num_handlers == 0:
            return None
        if num_handlers == 1:
            return handlers[0]
        raise Exception("more than one handler for '" + metric_name + "': " + handlers)

    def query_type_handler(self, metric_name, tags):
        # Split out the query type from the rest of the metric name
        metric_name_parts = metric_name.rsplit('.', 1)
        query_type = metric_name_parts[1]

        orig_metric_name = metric_name
        metric_name = metric_name_parts[0]

        all_tags = tags + ['query_type:' + query_type]
        self.log.debug(
            'translating query type metric %s to %s (query_type: %s)', orig_metric_name, metric_name, query_type
        )
        self.log.debug('all_tags: %s', all_tags)

        return metric_name, all_tags

    def query_class_handler(self, metric_name, tags):
        # Split out the query class from the rest of the metric name
        metric_name_parts = metric_name.rsplit('.', 1)
        query_class = metric_name_parts[1]

        orig_metric_name = metric_name
        metric_name = metric_name_parts[0]

        all_tags = tags + ['query_class:' + query_class]
        self.log.debug(
            'translating query class metric %s to %s (query_class: %s)', orig_metric_name, metric_name, query_class
        )
        self.log.debug('all_tags: %s', all_tags)

        return metric_name, all_tags

    def query_opcode_handler(self, metric_name, tags):
        # Split out the query opcode from the rest of the metric name
        metric_name_parts = metric_name.rsplit('.', 1)
        opcode = metric_name_parts[1]

        orig_metric_name = metric_name
        metric_name = metric_name_parts[0]

        all_tags = tags + ['opcode:' + opcode]
        self.log.debug('translating query opcode metric %s to %s (opcode: %s)', orig_metric_name, metric_name, opcode)
        self.log.debug('all_tags: %s', all_tags)

        return metric_name, all_tags

    def query_flags_handler(self, metric_name, tags):
        # Split out the query flag from the rest of the metric name
        metric_name_parts = metric_name.rsplit('.', 1)
        flag = metric_name_parts[1]

        orig_metric_name = metric_name
        metric_name = metric_name_parts[0]

        all_tags = tags + ['flag:' + flag]
        self.log.debug('translating query flag metric %s to %s (flag: %s)', orig_metric_name, metric_name, flag)
        self.log.debug('all_tags: %s', all_tags)

        return metric_name, all_tags

    def answer_rcode_handler(self, metric_name, tags):
        # Split out the rcode from the rest of the metric name
        metric_name_parts = metric_name.rsplit('.', 1)
        rcode = metric_name_parts[1]

        # Handle e.g. num.answer.rcode.NOERROR, but leave
        # num.answer.rcode.nodata along since it's special.
        if rcode == 'nodata':
            return metric_name, tags

        orig_metric_name = metric_name
        metric_name = metric_name_parts[0]

        all_tags = tags + ['rcode:' + rcode]
        self.log.debug('translating num.answer.rcode %s to %s (rcode: %s)', orig_metric_name, metric_name, rcode)
        self.log.debug('all_tags: %s', all_tags)

        return metric_name, all_tags

    def thread_handler(self, metric_name, tags):
        # There are separate counters for each thread.  If we don't do any
        # massaging, it's difficult to define the complete set of possible
        # metrics that we might generate.  Instead, remove the thread number
        # from the metric name, and add it as a tag.

        # Split the first part of the metric name (e.g. thread0) from the rest
        metric_name_parts = metric_name.split('.', 1)
        thread = metric_name_parts[0]

        # Grab the actual thread number
        thread_num = thread[len('thread') :]

        # Rebuild the metric name without the thread number
        orig_metric_name = metric_name
        metric_name = 'thread.' + metric_name_parts[1]

        # Add the thread number as a tag
        all_tags = tags + ['thread:' + thread_num]

        self.log.debug('translating thread metric %s to %s (thread_num: %s)', orig_metric_name, metric_name, thread_num)
        self.log.debug('all_tags: %s', all_tags)

        return metric_name, all_tags

    def metric_name_to_tags(self, metric_name, tags):
        """Returns a tuple (metric_name, all_tags) where all_tags are the tags provided
        to the check, with any additional for this metric if there are any
        """
        # Some metrics from unbound make more sense to handle as name + tag in
        # datadog.  If nothing else, it makes metadata.csv more compact, but
        # also more predictable/future proof, as some metric names are dynamic.
        handler = self.tag_handler(metric_name)
        if handler is not None:
            metric_name, all_tags = handler(metric_name, tags)
        else:
            all_tags = tags

        return metric_name, all_tags


# From https://stackoverflow.com/a/377028.  Once we can depend on python
# 3.x, use shutil.which
def which(program, use_sudo, log):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    if use_sudo:
        # Pass raise_on_empty_output as False to Leave it to the caller to handle the not
        # found case.
        stdout, stderr, returncode = get_subprocess_output(['sudo', 'which', program], log, raise_on_empty_output=False)
        if returncode == 0:
            return stdout

        for line in stderr.splitlines():
            log.debug('stderr from sudo which %s: %s', program, line)

        return None

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
