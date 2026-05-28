# (C) voseghale 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""
Linux PSI (Pressure Stall Information) check.

Reads /proc/pressure/{cpu,memory,io} (Linux kernel 4.20+) and emits per-resource
some/full avg10/avg60/avg300 (gauges, percent) and total (monotonic_count,
microseconds) metrics. Gracefully handles older kernels where /proc/pressure/cpu
does not have a `full` line (added in kernel 5.13) or where PSI is not enabled
at all (boot parameter `psi=1` not set).

The check namespace is `system.pressure.` to slot alongside Datadog's existing
`system.*` Linux metrics (cpu, memory, io, processes).

See https://docs.kernel.org/accounting/psi.html for the kernel feature.
"""
from __future__ import annotations

import os

from datadog_checks.base import AgentCheck

try:
    # Available inside the Agent runtime; not in unit tests on a bare interpreter.
    import datadog_agent
except ImportError:  # pragma: no cover - exercised only by Agent runtime
    datadog_agent = None


PRESSURE_FILES = ('cpu', 'memory', 'io')
VALID_KINDS = ('some', 'full')
AVG_KEYS = ('avg10', 'avg60', 'avg300')


class LinuxPSICheck(AgentCheck):
    """Read /proc/pressure/* and emit PSI metrics."""

    SERVICE_CHECK_NAME = 'linux_psi.can_read'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = list(self.instance.get('tags', []))
        self._set_paths()

    def _set_paths(self):
        """Resolve the pressure directory, honoring the Agent's procfs_path
        config so container deployments that mount /proc at /host/proc work
        out of the box."""
        proc_location = '/proc'
        if datadog_agent is not None:
            configured = datadog_agent.get_config('procfs_path')
            if configured:
                proc_location = configured
        self.pressure_dir = os.path.join(proc_location.rstrip('/'), 'pressure')

    def check(self, _):
        if not os.path.isdir(self.pressure_dir):
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.WARNING,
                tags=self.tags,
                message=(
                    'PSI is not enabled on this kernel. PSI requires Linux 4.20+ '
                    'and the kernel must be booted with `psi=1` if the distro '
                    'disables it by default. See the integration README for '
                    'enabling it.'
                ),
            )
            return

        emitted = False
        worst_status = AgentCheck.OK
        worst_message = ''
        for resource in PRESSURE_FILES:
            path = os.path.join(self.pressure_dir, resource)
            try:
                self._read_one(resource, path)
                emitted = True
            except FileNotFoundError:
                # One of the three may be missing on some kernels (e.g. io
                # in restricted cgroups). Not an error overall.
                self.log.debug('PSI file not found: %s', path)
            except PermissionError as e:
                worst_status = AgentCheck.CRITICAL
                worst_message = f'Permission denied reading {path}: {e}'
            except OSError as e:
                # Soft-fail on other IO errors; report them but keep going.
                self.log.warning('Error reading %s: %s', path, e)

        if worst_status == AgentCheck.CRITICAL:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL,
                               tags=self.tags, message=worst_message)
        elif emitted:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK,
                               tags=self.tags)
        else:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.WARNING,
                tags=self.tags,
                message='No PSI files could be read; nothing emitted.',
            )

    def _read_one(self, resource, path):
        """Open one /proc/pressure/<resource> file and emit each line's metrics."""
        with open(path, 'r') as f:
            for line in f:
                self._emit_line(resource, line.strip())

    def _emit_line(self, resource, line):
        """Parse a line like:
            'some avg10=0.18 avg60=0.09 avg300=0.04 total=294183'
        and emit one metric per field, tagged with the resource (cpu/memory/io)
        and kind (some/full).
        """
        if not line:
            return
        parts = line.split()
        if not parts:
            return
        kind = parts[0]
        if kind not in VALID_KINDS:
            self.log.debug('Skipping unknown PSI line for %s: %s', resource, line)
            return
        metric_prefix = f'system.pressure.{resource}.{kind}'
        for field in parts[1:]:
            if '=' not in field:
                continue
            key, value = field.split('=', 1)
            try:
                fval = float(value)
            except ValueError:
                self.log.debug('Non-numeric PSI value %s=%s', key, value)
                continue
            if key in AVG_KEYS:
                self.gauge(f'{metric_prefix}.{key}', fval, tags=self.tags)
            elif key == 'total':
                # `total` is microseconds since boot; emit as monotonic_count
                # so Datadog computes the per-interval rate automatically.
                self.monotonic_count(f'{metric_prefix}.total', fval,
                                     tags=self.tags)
            else:
                self.log.debug('Skipping unknown PSI field %s=%s', key, value)
