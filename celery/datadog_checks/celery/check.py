# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from typing import Any, Mapping, Dict, List  # noqa: F401

import celery.app.control
from celery import Celery
from datadog_checks.base import AgentCheck, ConfigurationError  # noqa: F401

_WORKERS_CRIT_MAX_DEFAULT = 5

metric_map: Mapping[str, str] = {
    "SVC_CHECK": 'ping',
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

        if "report_task_count" in self.instance and not isinstance(self.instance.get("report_task_count"), bool):
            raise ConfigurationError("Instance incorrectly configured")

        if "report_rusage" in self.instance and not isinstance(self.instance.get("report_rusage"), bool):
            raise ConfigurationError("Instance incorrectly configured")

        if "workers_crit_max" in self.instance and not isinstance(self.instance.get("workers_crit_max"), int):
            raise ConfigurationError("Instance incorrectly configured")

        self._remembered_workers: Dict[str, int] = {}
        self._app: str = self.instance.get("app")
        self._broker: str = self.instance.get("broker")
        self._remember_workers: bool = "remember_workers" in self.instance and self.instance.get("remember_workers")
        self._report_task_count: bool = "report_task_count" in self.instance and self.instance.get("report_task_count")
        self._report_rusage: bool = "report_rusage" in self.instance and self.instance.get("report_rusage")
        self._workers_crit_max: int = \
            int(self.instance.get("workers_crit_max")) if "workers_crit_max" in self.instance \
            else _WORKERS_CRIT_MAX_DEFAULT

    def check(self, _):
        app: Celery = Celery(self._app, broker=self._broker)
        self._check_worker_ping(app)
        inspect: celery.app.control.Inspect = app.control.inspect()
        self._check_task_metrics(inspect)
        self._check_worker_metrics(inspect)

    def _check_worker_ping(self, app: Celery) -> None:
        active_workers: List[str] = []
        for worker_status in app.control.ping():
            for name, value in worker_status.items():
                self.service_check(metric_map["SVC_CHECK"],
                                   self.OK if value['ok'] == 'pong' else self.CRITICAL,
                                   tags=[f"worker:{name}", f"app:{self._app}"],
                                   )
                if self._remember_workers:
                    self._remembered_workers[name] = 0
                    active_workers.append(name)
        if self._remember_workers:
            # we check if all workers we discovered earlier pinged this time,
            # if one didn't report, we report 'critical' for it
            # if we reported critical for a certain amount of times in a row, we assume the worker is gone for good
            # and remove it from the list
            for worker in list(self._remembered_workers.keys()):
                if worker not in active_workers:
                    self.service_check(metric_map["SVC_CHECK"],
                                       self.CRITICAL,
                                       tags=[f"worker:{worker}", f"app:{self._app}"],
                                       )
                    self._remembered_workers[worker] += 1
                    if self._remembered_workers[worker] >= self._workers_crit_max:
                        del self._remembered_workers[worker]

    def _check_task_metrics(self, inspect: celery.app.control.Inspect) -> None:
        for worker, tasks in inspect.active().items():
            self.gauge(metric_map["ACTIVE_TASKS"], len(tasks), tags=[f"worker:{worker}", f"app:{self._app}"])
        for worker, tasks in inspect.scheduled().items():
            self.gauge(metric_map["SCHEDULED_TASKS"], len(tasks), tags=[f"worker:{worker}", f"app:{self._app}"])
        for worker, tasks in inspect.reserved().items():
            self.gauge(metric_map["RESERVED_TASKS"], len(tasks), tags=[f"worker:{worker}", f"app:{self._app}"])
        for worker, tasks in inspect.revoked().items():
            self.gauge(metric_map["REVOKED_TASKS"], len(tasks), tags=[f"worker:{worker}", f"app:{self._app}"])

    def _check_worker_metrics(self, inspect: celery.app.control.Inspect) -> None:
        # Send Worker Metrics
        for worker, stats in inspect.stats().items():
            self.gauge(metric_map["UPTIME"], stats['uptime'], tags=[f"worker:{worker}", f"app:{self._app}"])
            self.gauge(metric_map["PREFETCH_COUNT"],
                       stats["prefetch_count"],
                       tags=[f"worker:{worker}", f"app:{self._app}"])
            # Report number of tasks that have been accepted per type since worker-startup
            if self._report_task_count:
                for task, count in stats['total'].items():
                    self.gauge(metric_map["TASK_COUNT"],
                               count,
                               tags=[f"worker:{worker}", f"task:{task}", f"app:{self._app}"]
                               )
            # Report rusage values per worker
            if self._report_rusage:
                for metric, value in stats['rusage'].items():
                    self.gauge(f"{metric_map['RUSAGE']}.{metric}", value, tags=[f"worker:{worker}", f"app:{self._app}"])
