from __future__ import print_function

from collections import Counter, defaultdict, deque
from datetime import datetime

from dateutil import parser

from datadog_checks.checks import AgentCheck
from datadog_checks.errors import ConfigurationError

from .lib import APIClient

EVENT_TYPE = 'docker'
EXIT_SERVICE_CHECK_NAME = 'docker.exit'
TAG_NAMES = {
    'container': ["docker_image", "short_image", "image_name", "image_tag"],
    'performance': ["container_name", "docker_image", "image_name", "image_tag"],
    'image': ['image_name', 'image_tag'],
}


class WinDockerDaemonCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):

        if instances is not None and len(instances) > 1:
            raise Exception("Docker check only supports one configured instance.")

        self.client = None

        # Tag options
        self.tag_names = TAG_NAMES
        self.custom_tags = set()
        self.collect_labels_as_tags = True
        self.event_attributes_as_tags = []

        # Event options
        self.collect_events = True
        self.event_last_date_checked = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds())
        self.filtered_event_types = ('exec_create', 'exec_start', 'exec_die')

        # Other options
        # self.collect_image_stats = True
        # self.collect_container_size = True
        self.collect_container_count = True
        # self.collect_volume_count = True
        # self.collect_image_size = True
        # self.collect_disk_stats = True
        self.collect_exit_codes = True

        AgentCheck.__init__(self, name, init_config, agentConfig, instances=instances)

        self.init_success = False

    def check(self, instance):
        self.custom_tags = set(instance.get("tags", []))
        url = instance.get('url')

        if not url:
            raise ConfigurationError(
                'Configuration error, No \'url\' found in config.  Please fix win_docker_daemon conf.yaml'
            )

        self.client = instance.get("test_api_client", APIClient(base_url=url, logger=self.log))

        # node info @TODO
        # docker_swarm_node_role

        # List all containers
        all_containers = self.client.containers()
        all_containers_by_id = {i['Id']: i for i in all_containers}

        # Container counts
        self._process_container_totals(all_containers)
        self._process_container_counts(all_containers)

        # Container events
        self._process_events(all_containers_by_id)

        # Volume metrics @TODO

        # Image metrics @TODO

        # Container cpu, net, mem metrics for running containers
        self._process_stat_metrics(all_containers_by_id)

    # simplified docker_daemon
    def _process_container_totals(self, all_containers):
        if not self.collect_container_count:
            return

        tags = self.custom_tags.copy()
        counts = Counter(c['State'] for c in all_containers)

        if 'running' in counts.keys():
            AgentCheck.gauge(self, 'docker.containers.running.total', counts['running'], tags=tags)

        if 'exited' in counts.keys():
            AgentCheck.gauge(self, 'docker.containers.stopped.total', counts['exited'], tags=tags)

    def _process_container_counts(self, all_containers):
        if not self.collect_container_count:
            return

        aggregated_images = defaultdict(list)
        for container in all_containers:
            aggregated_images[container['Image']].append(container)

        for image_name, containers in aggregated_images.items():
            counts = Counter(c['State'] for c in containers)
            for state, count in counts.items():
                tags = self.custom_tags.copy()
                tags.add(":".join(["image_name", image_name]))
                tags.add(":".join(["docker_image", image_name]))

                if state == 'running':
                    AgentCheck.gauge(self, 'docker.containers.running', count, tags=tags)

                if state == 'exited':
                    AgentCheck.gauge(self, 'docker.containers.stopped', count, tags=tags)

    # almost wholesale copy from docker_daemon
    def _process_events(self, all_containers_by_id):
        if not self.collect_events:
            return

        now = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds())

        try:
            events = self.client.events(since=self.event_last_date_checked, until=now)
            if len(events) > 0:
                self.event_last_date_checked = events[-1]['time']
            self._report_exit_codes(events, all_containers_by_id)

            aggregated_events = self.get_aggregated_events(events)
            dd_events = self._format_events(aggregated_events, all_containers_by_id)

            for event in dd_events:
                self.log.debug("Creating event: %s" % event['msg_title'])
                self.event(event)
        except Exception as ex:
            self.log.error(ex)

    def _process_stat_metrics(self, all_containers_by_id):
        for container_id, container in all_containers_by_id.items():
            try:
                if container['State'] != "running":
                    continue

                stats = self.client.stats(container_id)

                tags = self.custom_tags.copy()
                tags.update(self._get_tags_from_container(container))
                tags.add('container_name:%s' % container['Names'][0])

                # cpu metrics
                cpu_stats = calculate_cpu_percent(stats)
                AgentCheck.gauge(self, 'docker.cpu.usage', cpu_stats["total"], tags=tags)
                AgentCheck.histogram(self, 'docker.cpu.usage', cpu_stats["total"], tags=tags)

                AgentCheck.gauge(self, 'docker.cpu.system', cpu_stats["system"], tags=tags)
                AgentCheck.histogram(self, 'docker.cpu.system', cpu_stats["system"], tags=tags)
                AgentCheck.gauge(self, 'docker.cpu.user', cpu_stats["user"], tags=tags)
                AgentCheck.histogram(self, 'docker.cpu.user', cpu_stats["user"], tags=tags)

                # mem metrics
                AgentCheck.gauge(self, 'docker.mem.commit', stats["memory_stats"]["commitbytes"], tags=tags)
                AgentCheck.histogram(self, 'docker.mem.commit', stats["memory_stats"]["commitbytes"], tags=tags)
                AgentCheck.gauge(self, 'docker.mem.rss', stats["memory_stats"]["privateworkingset"], tags=tags)
                AgentCheck.histogram(self, 'docker.mem.rss', stats["memory_stats"]["privateworkingset"], tags=tags)

                # network metrics
                for interface_name, network in stats["networks"].items():
                    tags.add(":".join(["docker_network", interface_name]))

                    AgentCheck.rate(self, 'docker.net.bytes_rcvd', network["rx_bytes"], tags=tags)
                    # AgentCheck.histogram(self, 'docker.net.bytes_rcvd', network["rx_bytes"], tags=tags)

                    AgentCheck.rate(self, 'docker.net.bytes_sent', network["tx_bytes"], tags=tags)
                    # AgentCheck.histogram(self, 'docker.net.bytes_sent', network["tx_bytes"], tags=tags)

                # storage stats @TODO

            except Exception as ex:
                self.log.error(ex)

    def _report_exit_codes(self, api_events, all_containers_by_id):
        # almost wholesale copy from docker_daemon'''
        if not self.collect_exit_codes:
            return

        for event in api_events:
            container_tags = set()
            container = all_containers_by_id.get(event.get('id'))

            if container is None:
                continue

            # Only continue reporting if there is a die event
            if not event['status'].startswith('exec_die'):
                continue

            container_tags.update(self._get_tags_from_container(container))
            container_tags.add('container_name:%s' % container['Names'][0])
            try:
                exit_code = int(event['Actor']['Attributes']['exitCode'])
                message = 'Container %s exited with %s' % (container['Names'][0], exit_code)
                status = AgentCheck.OK if exit_code == 0 else AgentCheck.CRITICAL
                self.service_check(EXIT_SERVICE_CHECK_NAME, status, tags=list(container_tags), message=message)
            except KeyError:
                self.log.warning('Unable to collect the exit code for container %s' % container['Names'][0])

    def get_aggregated_events(self, api_events):
        # simplified from originaldocker_daemon
        aggregated_events = defaultdict(deque)
        for event in api_events:
            if 'id' not in event:
                continue

            image_name = event['from'].replace('sha256:', '')
            aggregated_events[image_name].appendleft(event)

        return aggregated_events

    def _format_events(self, aggregated_events, all_containers_by_id):
        # almost wholesale copy from docker_daemon
        events = []
        for image_name, event_group in aggregated_events.items():
            container_tags = set()
            filtered_events_count = 0
            normal_prio_events = []

            for event in event_group:
                # Only keep events that are not configured to be filtered out
                if not event['status'].startswith(self.filtered_event_types):
                    filtered_events_count += 1
                    continue
                container_name = event['id'][:11]

                if event['id'] in all_containers_by_id:
                    container = all_containers_by_id[event['id']]
                    container_name = container["Names"][0]
                    container_tags.update(self._get_tags_from_container(container))
                    container_tags.add('container_name:%s' % container_name)

                normal_prio_events.append((event, container_name))

            if filtered_events_count:
                self.log.debug('%d events were filtered out because of ignored event type' % filtered_events_count)

            normal_event = self._create_dd_event(normal_prio_events, image_name, container_tags, priority='Normal')
            if normal_event:
                events.append(normal_event)

        return events

    def _create_dd_event(self, events, image, c_tags, priority='Normal'):
        # almost wholesale copy from docker_daemon
        if not events:
            return

        max_timestamp = 0
        status = defaultdict(int)
        status_change = []

        for ev, c_name in events:
            max_timestamp = max(max_timestamp, int(ev['time']))
            status[ev['status']] += 1
            status_change.append([c_name, ev['status']])

        status_text = ", ".join(["%d %s" % (count, st) for st, count in status.items()])
        msg_title = "%s %s on %s" % (image, status_text, self.hostname)
        msg_body = ("%%%\n" "{image_name} {status} on {hostname}\n" "```\n{status_changes}\n```\n" "%%%").format(
            image_name=image,
            status=status_text,
            hostname=self.hostname,
            status_changes="\n".join(["%s \t%s" % (change[1].upper(), change[0]) for change in status_change]),
        )

        if any(error in status_text for error in ['oom', 'kill']):
            alert_type = "error"
        else:
            alert_type = None

        return {
            'timestamp': max_timestamp,
            'host': self.hostname,
            'event_type': EVENT_TYPE,
            'msg_title': msg_title,
            'msg_text': msg_body,
            'source_type_name': EVENT_TYPE,
            'event_object': 'docker:%s' % image,
            'tags': list(c_tags),
            'alert_type': alert_type,
            'priority': priority,
        }

    def _get_tags_from_container(self, container):
        # pull from container.labels if exist
        # what about swarm?
        tags = set()
        tags.add(':'.join(["container_name", container['Names'][0]]))
        tags.add(':'.join(["image_name", container['Image']]))
        tags.add(':'.join(["docker_image", container['Image']]))

        if self.collect_labels_as_tags:
            for k, v in container['Labels'].items():
                if len(v) == 0:
                    continue

                tags.add(':'.join([k, v]))

        return tags


def calculate_cpu_percent(stats):
    # port of helper functions from
    # https://github.com/moby/moby/blob/eb131c5383db8cac633919f82abad86c99bffbe5/cli/command/container/stats_helpers.go

    # Max number of 100 microsecond intervals between the previous time read and now
    pre_read = parser.parse(stats["preread"], ignoretz=True)
    read = parser.parse(stats["read"], ignoretz=True)
    poss_intervals = int((read - pre_read).total_seconds() * 1000000000)
    poss_intervals /= 100  # number of 100s int
    poss_intervals *= int(stats["num_procs"])

    # Intervals used
    total_used = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    system_used = (
        stats["cpu_stats"]["cpu_usage"]["usage_in_kernelmode"]
        - stats["precpu_stats"]["cpu_usage"]["usage_in_kernelmode"]
    )
    user_used = (
        stats["cpu_stats"]["cpu_usage"]["usage_in_usermode"] - stats["precpu_stats"]["cpu_usage"]["usage_in_usermode"]
    )

    # Percentage avoiding divide-by-zero
    if poss_intervals > 0:
        return {
            "total": float(total_used) / float(poss_intervals) * 100,
            "system": float(system_used) / float(poss_intervals) * 100,
            "user": float(user_used) / float(poss_intervals) * 100,
        }

    return {"total": 0.00, "system": 0.00, "user": 0.00}
