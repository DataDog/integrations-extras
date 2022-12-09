import collections
import datetime
import multiprocessing
import os
import time
from unittest import mock

import psutil
import pytest
import requests
from requests.structures import CaseInsensitiveDict

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.filemage import FilemageCheck

from .common import EXPECTED_CHECKS


class MockProcess(object):
    def __init__(self, pid=None, name=None, create_time=None, ppid=None, cmdline=None, status='sleeping'):
        # if pid is not specified find an open one that won't be used by another proc
        if pid is None:
            p = multiprocessing.Process(target=lambda: time.sleep(1))
            p.start()
            self._pid = p.pid
            p.terminate()
        else:
            self._pid = pid
        self._name = name
        self._create_time = create_time if create_time is not None else datetime.datetime.now().timestamp()
        self._ppid = ppid if ppid is not None else os.getppid()
        self._cmdline = cmdline if cmdline is not None else [name]
        self._status = status

        self._gone = False
        self._pid_reused = False
        self._hash = None
        self.info = None

        self._exitcode = object()
        self._ident = (self.pid, self._create_time)

    def __str__(self):
        info = collections.OrderedDict()
        info["pid"] = self.pid
        if self._name:
            info['name'] = self._name
        with self.oneshot():
            try:
                info["name"] = self.name()
                info["status"] = self.status()
            except psutil.ZombieProcess:
                info["status"] = "zombie"
            except psutil.NoSuchProcess:
                info["status"] = "terminated"
            except psutil.AccessDenied:
                pass
            if self._exitcode not in (object, None):
                info["exitcode"] = self._exitcode
            if self._create_time:
                info['started'] = datetime.datetime.fromtimestamp(self._create_time).strftime('%Y-%m-%d %H:%M:%S')
            return "%s.%s(%s)" % (
                self.__class__.__module__,
                self.__class__.__name__,
                ", ".join(["%s=%r" % (k, v) for k, v in info.items()]),
            )

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, (MockProcess, psutil.Process)):
            return NotImplemented
        return self._ident == other._ident

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self._ident)
        return self._hash

    @property
    def pid(self):
        return self._pid

    def oneshot(self):
        raise NotImplementedError()

    def as_dict(self, attrs=None, ad_value=None):
        valid_names = {'pid', 'cmdline', 'create_time', 'name', 'status', 'ppid'}
        if attrs is not None:
            if not isinstance(attrs, (list, tuple, set, frozenset)):
                raise TypeError("invalid attrs type %s" % type(attrs))
            attrs = set(attrs)
            invalid_names = attrs - valid_names
            if invalid_names:
                raise ValueError(
                    "invalid attr name%s %s"
                    % ("s" if len(invalid_names) > 1 else "", ", ".join(map(repr, invalid_names)))
                )

        retdict = dict()
        ls = attrs or valid_names
        for name in ls:
            try:
                if name == 'pid':
                    ret = self.pid
                else:
                    meth = getattr(self, name)
                    ret = meth()
            except (psutil.AccessDenied, psutil.ZombieProcess):
                ret = ad_value
            except NotImplementedError:
                if attrs:
                    raise
                continue
            retdict[name] = ret
        return retdict

    def parent(self):
        return psutil.Process(self.ppid())

    def parents(self):
        raise NotImplementedError()

    def is_running(self):
        if self._gone or self._pid_reused:
            return False
        try:
            return not (self != psutil.Process(self.pid))
        except psutil.ZombieProcess:
            # We should never get here as it's already handled in
            # Process.__init__; here just for extra safety.
            return True
        except psutil.NoSuchProcess:
            self._gone = True
            return False

    def cmdline(self):
        return self._cmdline

    def status(self):
        return self._status

    def ppid(self):
        return self._ppid

    def name(self):
        return self._name

    def cwd(self):
        raise NotImplementedError()

    def username(self):
        raise NotImplementedError()

    def exe(self):
        raise NotImplementedError()

    def create_time(self):
        return self._create_time

    def nice(self, value=None):
        raise NotImplementedError()

    def uids(self):
        raise NotImplementedError()

    def gids(self):
        raise NotImplementedError()

    def terminal(self):
        raise NotImplementedError()

    def num_fds(self):
        raise NotImplementedError()

    def io_counters(self):
        raise NotImplementedError()

    def ionice(self, ioclass=None, value=None):
        raise NotImplementedError()

    def rlimit(self, resource, limits=None):
        raise NotImplementedError()

    def cpu_affinity(self, cpus=None):
        raise NotImplementedError()

    def cpu_num(self):
        raise NotImplementedError()

    def environ(self):
        raise NotImplementedError()

    def num_handles(self):
        raise NotImplementedError()

    def num_ctx_switches(self):
        raise NotImplementedError()

    def num_threads(self):
        raise NotImplementedError()

    def threads(self):
        raise NotImplementedError()

    def children(self, recursive=False):
        raise NotImplementedError()

    def cpu_percent(self, interval=None):
        raise NotImplementedError()

    def cpu_times(self):
        raise NotImplementedError()

    def memory_info(self):
        raise NotImplementedError()

    def memory_full_info(self):
        raise NotImplementedError()

    def memory_percent(self, memtype="rss"):
        raise NotImplementedError()

    def memory_maps(self, grouped=True):
        raise NotImplementedError()

    def open_files(self):
        raise NotImplementedError()

    def connections(self, kind='inet'):
        raise NotImplementedError()

    def send_signal(self, sig):
        raise NotImplementedError()

    def suspend(self):
        raise NotImplementedError()

    def resume(self):
        raise NotImplementedError()

    def terminate(self):
        raise NotImplementedError()

    def kill(self):
        raise NotImplementedError()

    def wait(self, timeout=None):
        raise NotImplementedError()


class MockResponse:
    __attrs__ = [
        "_content",
        "status_code",
        "headers",
        "url",
        "history",
        "encoding",
        "reason",
        "cookies",
        "elapsed",
        "request",
    ]

    def __init__(self, json_data, status_code):
        self._content = False
        self._content_consumed = False
        self._next = None
        self.status_code = status_code
        self.headers = CaseInsensitiveDict()
        self.raw = None
        self.url = None
        self.encoding = None
        self.history = []
        self.reason = None
        self.cookies = None
        self.elapsed = datetime.timedelta(0)
        self.request = None
        self.json_data = json_data

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    def __bool__(self):
        return self.ok

    def __nonzero__(self):
        return self.ok

    def __iter__(self):
        return self.iter_content(128)

    @property
    def ok(self):
        try:
            self.raise_for_status()
        except requests.HTTPError:
            return False
        return True

    @property
    def is_redirect(self):
        raise NotImplementedError()

    @property
    def is_permanent_redirect(self):
        raise NotImplementedError()

    @property
    def next(self):
        raise NotImplementedError()

    @property
    def apparent_encoding(self):
        raise NotImplementedError()

    def iter_content(self, *args, **kwargs):
        raise NotImplementedError()

    def iter_lines(self, *args, **kwargs):
        raise NotImplementedError()

    @property
    def content(self):
        raise NotImplementedError()

    @property
    def text(self):
        raise NotImplementedError()

    def json(self, **kwargs):
        return self.json_data

    @property
    def links(self):
        raise NotImplementedError()

    def raise_for_status(self):
        http_error_msg = ""
        if isinstance(self.reason, bytes):
            try:
                reason = self.reason.decode("utf-8")
            except UnicodeDecodeError:
                reason = self.reason.decode("iso-8859-1")
        else:
            reason = self.reason

        if 400 <= self.status_code < 500:
            http_error_msg = f"{self.status_code} Client Error: {reason} for url: {self.url}"

        elif 500 <= self.status_code < 600:
            http_error_msg = f"{self.status_code} Server Error: {reason} for url: {self.url}"

        if http_error_msg:
            raise requests.HTTPError(http_error_msg, response=self)

    def close(self):
        raise NotImplementedError()


def mockPrcoessIterServicesDown(attrs=None, ad_value=None):
    def procIterFormat(proc):
        proc.info = proc.as_dict(attrs=attrs, ad_value=ad_value)
        return proc

    yield procIterFormat(MockProcess(name='systemd', cmdline=['/sbin/init']))


def mockPrcoessIterServicesUp(attrs=None, ad_value=None):
    def procIterFormat(proc):
        proc.info = proc.as_dict(attrs=attrs, ad_value=ad_value)
        return proc

    yield procIterFormat(MockProcess(name='systemd', cmdline=['/sbin/init']))
    yield procIterFormat(
        MockProcess(
            name='postgres',
            cmdline=[
                '/usr/lib/postgresql/12/bin/postgres',
                '-D',
                '/var/lib/postgresql/12/main',
                '-c',
                'config_file=/etc/postgresql/12/main/postgresql.conf',
            ],
        )
    )
    yield procIterFormat(
        MockProcess(
            name='gateway',
            cmdline=[
                '/opt/filemage/bin/gateway',
                '-c',
                '/etc/filemage/config.yml',
            ],
        )
    )


def mockRequestsGetMetricsDown(*args, **kwargs):
    return MockResponse({'message': 'Session expired.'}, 401)


def mockRequestsGetMetricsUp(*args, **kwargs):
    return MockResponse(
        [
            {'timestamp': '2022-12-09T17:00:10Z', 'path': '/tmp/example.csv', 'user': 'example', 'operation': 'put'},
            {'timestamp': '2022-12-09T17:00:10Z', 'path': '/tmp/example.csv', 'user': 'example', 'operation': 'rmdir'},
        ],
        200,
    )


@pytest.mark.unit
def test_bad_instance(dd_run_check, aggregator, bad_instance):
    with pytest.raises(ConfigurationError):
        c = FilemageCheck('filemage', {}, [bad_instance])
        dd_run_check(c)


@pytest.mark.unit
def test_good_instance(dd_run_check, aggregator, good_instance):
    c = FilemageCheck('filemage', {}, [good_instance])
    dd_run_check(c)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.filemage.check.requests.get', mockRequestsGetMetricsUp)
@mock.patch('datadog_checks.filemage.check.psutil.process_iter', mockPrcoessIterServicesUp)
def test_check_coverage(dd_run_check, aggregator, good_instance):
    c = FilemageCheck('filemage', {}, [good_instance])
    dd_run_check(c)
    for check in EXPECTED_CHECKS:
        aggregator.assert_service_check(check)
    aggregator.assert_no_duplicate_service_checks()


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.filemage.check.requests.get', mockRequestsGetMetricsUp)
@mock.patch('datadog_checks.filemage.check.psutil.process_iter', mockPrcoessIterServicesUp)
def test_metric_coverage(dd_run_check, aggregator, good_instance):
    c = FilemageCheck('filemage', {}, [good_instance])
    dd_run_check(c)
    for metric in FilemageCheck.FTP_TRACKED_METRICS:
        aggregator.assert_metric(metric)
    aggregator.assert_no_duplicate_metrics()
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(FilemageCheck.TRACKED_METRICS_META)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.filemage.check.psutil.process_iter', mockPrcoessIterServicesDown)
def test_services_down(dd_run_check, aggregator, good_instance):
    c = FilemageCheck('filemage', {}, [good_instance])
    dd_run_check(c)
    aggregator.assert_service_check('filemage.services_up', AgentCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.filemage.check.psutil.process_iter', mockPrcoessIterServicesUp)
def test_services_up(dd_run_check, aggregator, good_instance):
    c = FilemageCheck('filemage', {}, [good_instance])
    dd_run_check(c)
    aggregator.assert_service_check('filemage.services_up', AgentCheck.OK)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.filemage.check.requests.get', mockRequestsGetMetricsDown)
@mock.patch('datadog_checks.filemage.check.psutil.process_iter', mockPrcoessIterServicesUp)
def test_metrics_down(dd_run_check, aggregator, good_instance):
    c = FilemageCheck('filemage', {}, [good_instance])
    dd_run_check(c)
    aggregator.assert_service_check('filemage.metrics_up', AgentCheck.WARNING)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.filemage.check.requests.get', mockRequestsGetMetricsUp)
@mock.patch('datadog_checks.filemage.check.psutil.process_iter', mockPrcoessIterServicesUp)
def test_metrics_up(dd_run_check, aggregator, good_instance):
    c = FilemageCheck('filemage', {}, [good_instance])
    dd_run_check(c)
    aggregator.assert_service_check('filemage.metrics_up', AgentCheck.OK)
