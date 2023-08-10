# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import logging
import re
from typing import Any, Dict, List, Mapping  # noqa: F401

import celery.app.control
from celery import Celery
from datadog_checks.base import AgentCheck, ConfigurationError  # noqa: F401

_WORKERS_CRIT_MAX_DEFAULT = 5
_PING_TIMEOUT = 5.0
_INSPECT_TIMEOUT = 5.0
logger = logging.getLogger(__name__)

metric_map: Mapping[str, str] = {
    "SVC_CHECK": 'ping',
    "ACTIVE": 'active',
    "ACTIVE_TASKS": 'tasks.active',
    "RESERVED_TASKS": 'tasks.reserved',
    "REVOKED_TASKS": 'tasks.revoked',
    "SCHEDULED_TASKS": 'tasks.scheduled',
    "UPTIME": 'uptime',
    "PREFETCH_COUNT": 'prefetch_count',
    "TASK_COUNT": 'task_count',
    "RUSAGE": 'rusage',
}


class CeleryCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'celery.worker'

    def __init__(self, name, init_config, instances):
        super(CeleryCheck, self).__init__(name, init_config, instances)

        if "app" not in self.instance or "broker" not in self.instance:
            raise ConfigurationError("Instance configuration insufficient. Add 'app' and 'broker'.")

        if "remember_workers" in self.instance and not isinstance(self.instance.get("remember_workers"), bool):
            raise ConfigurationError("Instance incorrectly configured")

        if "workers_crit_max" in self.instance and not isinstance(self.instance.get("workers_crit_max"), int):
            raise ConfigurationError("Instance incorrectly configured")

        self._remembered_workers: Dict[str, int] = {}
        self._app: str = self.instance.get("app")
        self._broker: str = self.instance.get("broker")
        self._remember_workers: bool = "remember_workers" in self.instance and self.instance.get("remember_workers")
        self._workers_crit_max: int = (
            int(self.instance.get("workers_crit_max"))
            if "workers_crit_max" in self.instance
            else _WORKERS_CRIT_MAX_DEFAULT
        )

        self._group_regexes: List[str] = self.instance.get("group_regexes") if "group_regexes" in self.instance else []
        self._expected_workers: List[str] = []
        if "expected_workers" in self.instance:
            if isinstance(self.instance.get("expected_workers"), List):
                self._expected_workers = self.instance.get("expected_workers")
            elif isinstance(self.instance.get("expected_workers"), str):
                self._expected_workers = [self.instance.get("expected_workers")]
            else:
                raise ConfigurationError("'expected_workers' needs to be a list of strings or string")

        self._tags: List[str] = []
        if "tags" in self.instance:
            if isinstance(self.instance.get("tags"), List):
                self._tags = self.instance.get("tags")
            elif isinstance(self.instance.get("tags"), str):
                self._tags = [self.instance.get("tags")]
            else:
                raise ConfigurationError("'tags' needs to be a list of strings or string")
        self._tags.append(f"app:{self._app}")
        self._tag_cache = {}

    def check(self, _):
        app: Celery = Celery(self._app, broker=self._broker)
        self._check_worker_ping(app)
        inspect: celery.app.control.Inspect = app.control.inspect(timeout=_INSPECT_TIMEOUT)
        self._check_task_metrics(inspect)
        self._check_worker_metrics(inspect)

    def _check_worker_ping(self, app: Celery) -> None:
        active_workers: List[str] = []
        for worker_status in app.control.ping(timeout=_PING_TIMEOUT):
            for name, value in worker_status.items():
                tags = self._gen_tags(worker=name)
                if 'ok' in value and value['ok'] == 'pong':
                    self.service_check(metric_map["SVC_CHECK"], self.OK, tags=tags)
                    self.gauge(metric_map["ACTIVE"], 1, tags=tags)
                    if self._remember_workers:
                        self._remembered_workers[name] = 0
                    active_workers.append(name)
                else:
                    logger.debug(f"Worker not pinging properly: {name}: {value}")
                    self.service_check(metric_map["SVC_CHECK"], self.CRITICAL, tags=tags)
                    self.gauge(metric_map["ACTIVE"], 0, tags=tags)
                    if self._remember_workers:
                        self._remembered_workers[name] = 0
        if self._remember_workers:
            # we check if all workers we discovered earlier pinged this time,
            # if one didn't report, we report 'critical' for it
            # if we reported critical for a certain amount of times in a row, we assume the worker is gone for good
            # and remove it from the list
            for worker in list(self._remembered_workers.keys()):
                if worker not in active_workers:
                    self.service_check(metric_map["SVC_CHECK"], self.CRITICAL, tags=self._gen_tags(worker=worker))
                    self._remembered_workers[worker] += 1
                    logger.debug(f"No response from worker '{worker}'")
                    if self._remembered_workers[worker] >= self._workers_crit_max:
                        del self._remembered_workers[worker]
                        logger.info(f"Worker '{worker}' did not respond {self._workers_crit_max} times and was removed "
                                    "from the list of remembered workers")
        for worker in self._expected_workers:
            if worker not in active_workers:
                self.service_check(metric_map["SVC_CHECK"], self.CRITICAL, tags=self._gen_tags(worker=worker))
                logger.debug(f"Expected worker '{worker}' did not ping")

    def _check_task_metrics(self, inspect: celery.app.control.Inspect) -> None:
        for worker, tasks in inspect.active().items():
            self.gauge(metric_map["ACTIVE_TASKS"], len(tasks), tags=self._gen_tags(worker=worker))
        for worker, tasks in inspect.scheduled().items():
            self.gauge(metric_map["SCHEDULED_TASKS"], len(tasks), tags=self._gen_tags(worker=worker))
        for worker, tasks in inspect.reserved().items():
            self.gauge(metric_map["RESERVED_TASKS"], len(tasks), tags=self._gen_tags(worker=worker))
        for worker, tasks in inspect.revoked().items():
            self.gauge(metric_map["REVOKED_TASKS"], len(tasks), tags=self._gen_tags(worker=worker))

    def _check_worker_metrics(self, inspect: celery.app.control.Inspect) -> None:
        # Send Worker Metrics
        for worker, stats in inspect.stats().items():
            tags = self._gen_tags(worker=worker)
            self.gauge(metric_map["UPTIME"], stats['uptime'], tags=tags)
            self.gauge(metric_map["PREFETCH_COUNT"], stats["prefetch_count"], tags=tags)
            # Report number of tasks that have been accepted per type since worker-startup
            for task, count in stats['total'].items():
                self.gauge(metric_map["TASK_COUNT"], count, tags=tags + [f"task:{task}"])
            # Report rusage values per worker
            for metric, value in stats['rusage'].items():
                self.gauge(f"{metric_map['RUSAGE']}.{metric}", value, tags=tags)

    def _gen_tags(self, worker: str = "") -> List[str]:
        if worker:
            if worker not in self._tag_cache:
                t = self._tags.copy()
                t.append(f"worker:{worker}")

                # evaluate all grouping-regexes
                for regex in self._group_regexes:
                    m = re.match(regex, worker)
                    if m:
                        # check if we have named groups
                        group_dict = m.groupdict()
                        if group_dict:
                            # check each named group
                            for tag in group_dict.keys():
                                # check if the group should be converted into a named tag, or not
                                if not tag.startswith('ungrouped'):
                                    # convert named group into a named tag
                                    t.append(f"{tag}:{group_dict[tag]}")
                                else:
                                    # add tag without the group name
                                    t.append(group_dict[tag])
                        else:
                            # we only have un-named groups, so we add them as they are
                            for tag in m.groups():
                                t.append(tag)
                    else:
                        # if the regex didn't match, we print a warning, this will be printed only once for each worker
                        self.warning(f"The group-regex '{regex}' didn't match worker '{worker}'")

                self._tag_cache[worker] = t
            tags = self._tag_cache[worker]
        else:
            tags = self._tags
        return tags
