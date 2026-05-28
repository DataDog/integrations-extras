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
import re

from datadog_checks.base import AgentCheck, ConfigurationError

try:
    # Available inside the Agent runtime; not in unit tests on a bare interpreter.
    import datadog_agent
except ImportError:  # pragma: no cover - exercised only by Agent runtime
    datadog_agent = None


PRESSURE_FILES = ('cpu', 'memory', 'io')
VALID_KINDS = ('some', 'full')
AVG_KEYS = ('avg10', 'avg60', 'avg300')

# Matches major.minor.patch at the start of /proc/sys/kernel/osrelease.
# The string typically looks like '5.15.0-91-generic' or '6.5.0' or '4.4.302+'.
KERNEL_VERSION_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)')


class LinuxPSICheck(AgentCheck):
    """Read /proc/pressure/* and emit PSI metrics."""

    SERVICE_CHECK_NAME = 'linux_psi.can_read'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = list(self.instance.get('tags', []))
        self._resources = self._resolve_resources()
        self._set_paths()

    def _resolve_resources(self):
        """Return the tuple of PSI resources to collect for this instance.
        Defaults to all three; user can restrict via the `resources` config."""
        configured = self.instance.get('resources')
        if not configured:
            return PRESSURE_FILES
        invalid = [r for r in configured if r not in PRESSURE_FILES]
        if invalid:
            raise ConfigurationError(
                f'Unknown PSI resource(s) {invalid!r} in `resources` config. '
                f'Allowed values: {list(PRESSURE_FILES)}'
            )
        # Preserve user ordering, deduplicate.
        seen = set()
        result = []
        for r in configured:
            if r not in seen:
                seen.add(r)
                result.append(r)
        return tuple(result)

    def _set_paths(self):
        """Resolve the procfs root and the pressure directory, honoring the
        Agent's procfs_path config so container deployments that mount /proc
        at /host/proc work out of the box."""
        proc_location = '/proc'
        if datadog_agent is not None:
            configured = datadog_agent.get_config('procfs_path')
            if configured:
                proc_location = configured
        self._proc_root = proc_location.rstrip('/')
        self.pressure_dir = os.path.join(self._proc_root, 'pressure')

    @AgentCheck.metadata_entrypoint
    def _submit_kernel_version(self):
        """Surface the running kernel version as integration metadata so it
        appears in the tile's Integration metadata. Useful for fleet-wide
        audits like 'how many hosts are on a kernel that supports cpu.full
        PSI?' (added in 5.13)."""
        osrelease_path = os.path.join(self._proc_root, 'sys/kernel/osrelease')
        try:
            with open(osrelease_path, 'r') as f:
                raw = f.read().strip()
        except OSError as e:
            self.log.debug('Could not read kernel version from %s: %s',
                           osrelease_path, e)
            return

        m = KERNEL_VERSION_RE.match(raw)
        if not m:
            self.log.debug('Unexpected kernel version format: %r', raw)
            return
        major, minor, patch = m.groups()
        version = f'{major}.{minor}.{patch}'
        self.set_metadata(
            'version', version,
            scheme='semver',
            part_map={'major': major, 'minor': minor, 'patch': patch},
        )

    def check(self, _):
        self._submit_kernel_version()
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
        for resource in self._resources:
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
