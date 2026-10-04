# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datetime import datetime, timedelta
from json import JSONDecodeError
from time import monotonic
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from requests import Session
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, RequestException, Timeout

from datadog_checks.base import AgentCheck
from datadog_checks.base.constants import ServiceCheck
from datadog_checks.base.types import InitConfigType, InstanceType

from .config_models import ConfigMixin


class IbmB2bCheck(AgentCheck, ConfigMixin):
    __NAMESPACE__ = 'ibm_b2b'
    SERVICE_CHECK_NAME = 'can_connect'

    def __init__(self, name: str, init_config: InitConfigType, instances: list[InstanceType]) -> None:
        super().__init__(name, init_config, instances)
        self._seen_processes = {}

    def check(self, _: InstanceType) -> None:
        tags = list(self.config.tags or ())
        with Session() as session:
            try:
                auth_token, xsrf_token = self._sign_on(session)
            except (
                HTTPError,
                InvalidURL,
                ConnectionError,
                Timeout,
                RequestException,
                JSONDecodeError,
                ValueError,
                TypeError,
                AttributeError,
            ) as err:
                self.service_check(
                    self.SERVICE_CHECK_NAME,
                    ServiceCheck.CRITICAL,
                    tags=tags,
                    message=self._failure_message('signon', '/cdwebconsole/svc/signon', err),
                )
                return

            self.service_check(self.SERVICE_CHECK_NAME, ServiceCheck.OK, tags=tags)

            try:
                timezone_name = self.config.statistics_timezone
                if not timezone_name:
                    raise StatisticsTimezoneError(
                        'statistics_timezone is required; configure the Connect:Direct server IANA timezone'
                    )
                try:
                    server_timezone = ZoneInfo(timezone_name)
                except (TypeError, ValueError, ZoneInfoNotFoundError) as err:
                    raise StatisticsTimezoneError(
                        'statistics_timezone must be a valid IANA timezone for the Connect:Direct server'
                    ) from err

                stop_time = datetime.now(server_timezone)
                start_time = stop_time - timedelta(minutes=self.config.statistics_lookback_minutes)
                response = session.get(
                    f'{self.config.url}/cdwebconsole/svc/selectstatistics',
                    params={
                        'startTime': self._format_api_time(start_time),
                        'stopTime': self._format_api_time(stop_time),
                        'sortOrder': 'DESC',
                    },
                    headers={
                        'Authorization': auth_token,
                        'X-XSRF-TOKEN': xsrf_token,
                        'Content-Type': 'application/json; charset=utf-8',
                    },
                    verify=self.config.tls_verify,
                    timeout=self.config.timeout,
                )
                response.raise_for_status()
                records = response.json()
                self._submit_statistics(records, tags)
            except (
                HTTPError,
                InvalidURL,
                ConnectionError,
                Timeout,
                RequestException,
                JSONDecodeError,
                ValueError,
                TypeError,
                AttributeError,
            ) as err:
                self.service_check(
                    'statistics.can_collect',
                    ServiceCheck.CRITICAL,
                    tags=tags,
                    message=self._failure_message('selectstatistics', '/cdwebconsole/svc/selectstatistics', err),
                )
                return

            self.service_check('statistics.can_collect', ServiceCheck.OK, tags=tags)

    @staticmethod
    def _failure_message(operation, path, error):
        if isinstance(error, StatisticsTimezoneError):
            return str(error)
        if isinstance(error, HTTPError):
            status = error.response.status_code if error.response is not None else 'unknown'
            return f'{operation} failed with HTTP {status} at {path}'
        return f'{operation} failed ({type(error).__name__}) at {path}'

    def _sign_on(self, session: Session):
        response = session.post(
            f'{self.config.url}/cdwebconsole/svc/signon',
            json={
                'ipAddress': self.config.cd_node,
                'port': self.config.cd_port,
                'protocol': self.config.cd_protocol,
            },
            auth=(self.config.username, self.config.password),
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'X-XSRF-TOKEN': 'Y2hlY2tpdA==',
            },
            verify=self.config.tls_verify,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        if not self._signon_succeeded(response.json()):
            raise ValueError('sign-on response did not indicate success')

        authorization = response.headers.get('Authorization')
        xsrf_cookie = session.cookies.get('XSRF-TOKEN')
        session_cookie = session.cookies.get('JSESSIONID')
        if not authorization or not xsrf_cookie or not session_cookie:
            raise ValueError('sign-on response did not include required session tokens')

        return authorization, xsrf_cookie

    @staticmethod
    def _format_api_time(value: datetime) -> str:
        return value.strftime('%m/%d/%Y,%I:%M:%S %p').lower()

    def _submit_statistics(self, records, base_tags):
        if not isinstance(records, list):
            raise ValueError('statistics response must be a list')

        processes = {}
        transfers = {}
        for record in records:
            if not isinstance(record, dict) or not record.get('recordId'):
                continue
            if record.get('recordId') == 'totalRecords':
                continue

            process_name = str(record.get('processName') or '')
            secondary_node = record.get('secondaryNode') or ''
            if record.get('recordId') == 'CTRC':
                transfer = transfers.setdefault(
                    (process_name, secondary_node),
                    {'bytes_sent': 0, 'bytes_received': 0, 'has_bytes_sent': False, 'has_bytes_received': False},
                )
                for source, target, flag in (
                    ('bytesSent', 'bytes_sent', 'has_bytes_sent'),
                    ('bytesReceived', 'bytes_received', 'has_bytes_received'),
                ):
                    value = record.get(source)
                    if value is not None:
                        try:
                            transfer[target] += int(value)
                        except (TypeError, ValueError, OverflowError):
                            continue
                        transfer[flag] = True

            try:
                process_number = int(record.get('processNumber', 0))
            except (TypeError, ValueError, OverflowError):
                continue
            if process_number <= 0:
                continue

            process_key = (process_name, process_number)
            process = processes.setdefault(
                process_key,
                {
                    'failed': False,
                    'has_condition_code': False,
                    'secondary_node': secondary_node,
                },
            )
            if not process['secondary_node'] and secondary_node:
                process['secondary_node'] = secondary_node
            try:
                condition_code = int(record['conditionCode'])
            except (KeyError, TypeError, ValueError, OverflowError):
                continue
            process['has_condition_code'] = True
            if condition_code != 0:
                process['failed'] = True

        now = monotonic()
        retention_seconds = self.config.statistics_lookback_minutes * 2 * 60
        self._seen_processes = {
            key: first_seen for key, first_seen in self._seen_processes.items() if now - first_seen <= retention_seconds
        }

        grouped = {}
        for (process_name, _process_number), process in processes.items():
            process_key = (process_name, _process_number)
            if process_key in self._seen_processes:
                continue
            self._seen_processes[process_key] = now
            key = (process_name, process['secondary_node'])
            stats = grouped.setdefault(
                key,
                {
                    'total': 0,
                    'success': 0,
                    'failed': 0,
                    'bytes_sent': 0,
                    'bytes_received': 0,
                    'has_bytes_sent': False,
                    'has_bytes_received': False,
                },
            )
            stats['total'] += 1
            if process['failed']:
                stats['failed'] += 1
            elif process['has_condition_code']:
                stats['success'] += 1

        for (process_name, secondary_node), stats in grouped.items():
            metric_tags = list(base_tags)
            if process_name:
                metric_tags.append(f'process_name:{process_name}')
            if secondary_node:
                metric_tags.append(f'secondary_node:{secondary_node}')
            for name in ('total', 'success', 'failed'):
                self.gauge(f'processes.{name}', stats[name], tags=metric_tags)
        for (process_name, secondary_node), transfer in transfers.items():
            metric_tags = list(base_tags)
            if process_name:
                metric_tags.append(f'process_name:{process_name}')
            if secondary_node:
                metric_tags.append(f'secondary_node:{secondary_node}')
            if transfer['has_bytes_sent']:
                self.gauge('transfer.bytes_sent', transfer['bytes_sent'], tags=metric_tags)
            if transfer['has_bytes_received']:
                self.gauge('transfer.bytes_received', transfer['bytes_received'], tags=metric_tags)

    @staticmethod
    def _signon_succeeded(payload) -> bool:
        """Return true only for IBM's documented successful sign-on response."""
        if isinstance(payload, dict):
            payload = [payload]
        if not (
            isinstance(payload, list)
            and bool(payload)
            and isinstance(payload[0], dict)
            and str(payload[0].get('messageCode')) == '200'
        ):
            return False
        message = payload[0].get('message')
        if not isinstance(message, str) or 'signon' not in message.lower() or 'successful' not in message.lower():
            return False

        return True


class StatisticsTimezoneError(ValueError):
    pass
