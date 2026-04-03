"""Unit tests for the ClickHouse Cloud Datadog log check."""

import json
import time
from unittest.mock import MagicMock, patch

import pytest
import requests
from datadog_checks.clickhouse_cloud.check import (
    GAUGE_QUERY_LOG_ROWS,
    GAUGE_TEXT_LOG_ROWS,
    INTERNAL_USER_FILTER,
    SC_QUERY_LOG_CONNECT,
    SC_TEXT_LOG_CONNECT,
    TEXT_LOG_SQL,
    ClickHouseCloudCheck,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_check(instance):
    """Create a ClickHouseCloudCheck instance with the mock base class."""
    return ClickHouseCloudCheck('clickhouse_cloud', {}, [instance])


def _mock_query_response(rows):
    """Create a mock HTTP response returning JSONEachRow format."""
    response = MagicMock()
    response.status_code = 200
    response.text = '\n'.join(json.dumps(r) for r in rows)
    response.raise_for_status = MagicMock()
    return response


# ---------------------------------------------------------------------------
# Config validation tests
# ---------------------------------------------------------------------------


class TestConfigValidation:
    def test_invalid_batch_size_type_raises(self, default_instance):
        default_instance['log_batch_size'] = 'all'
        with pytest.raises(ValueError, match='log_batch_size must be an integer'):
            _make_check(default_instance)

    def test_batch_size_too_low_raises(self, default_instance):
        default_instance['log_batch_size'] = 0
        with pytest.raises(ValueError, match='log_batch_size must be between'):
            _make_check(default_instance)

    def test_batch_size_too_high_raises(self, default_instance):
        default_instance['log_batch_size'] = 99999
        with pytest.raises(ValueError, match='log_batch_size must be between'):
            _make_check(default_instance)

    def test_valid_batch_size_accepted(self, default_instance):
        default_instance['log_batch_size'] = 500
        check = _make_check(default_instance)
        assert check.batch_size == 500

    def test_invalid_slow_query_threshold_raises(self, default_instance):
        default_instance['slow_query_threshold_ms'] = -1
        with pytest.raises(ValueError, match='slow_query_threshold_ms must be between'):
            _make_check(default_instance)

    def test_invalid_backfill_minutes_raises(self, default_instance):
        default_instance['initial_backfill_minutes'] = 0
        with pytest.raises(ValueError, match='initial_backfill_minutes must be between'):
            _make_check(default_instance)

    def test_query_timeout_configurable(self, default_instance):
        default_instance['query_timeout_seconds'] = 60
        check = _make_check(default_instance)
        assert check.query_timeout_seconds == 60

    def test_query_timeout_default(self, default_instance):
        check = _make_check(default_instance)
        assert check.query_timeout_seconds == 30

    def test_missing_required_key_raises(self, default_instance):
        del default_instance['service_id']
        with pytest.raises(KeyError):
            _make_check(default_instance)


# ---------------------------------------------------------------------------
# Query log payload tests
# ---------------------------------------------------------------------------


class TestBuildQueryLogPayload:
    def test_normal_query_is_info(self, default_instance, query_log_rows):
        check = _make_check(default_instance)
        row = query_log_rows[0]  # type=QueryFinish, duration=120ms
        payload = check._build_query_log_payload(row)

        assert payload['status'] == 'info'
        assert payload['clickhouse.query_type'] == 'finish'
        assert payload['ddsource'] == 'clickhouse'
        assert payload['service'] == 'clickhouse'
        assert payload['clickhouse.query_id'] == 'abc-123-def-456'
        assert payload['clickhouse.user'] == 'default'
        assert payload['clickhouse.duration_ms'] == 120
        assert payload['clickhouse.query_kind'] == 'Select'
        assert payload['clickhouse.database'] == 'default'
        assert payload['clickhouse.written_bytes'] == 0
        assert payload['message'] == row['query']

    def test_slow_query_is_warning(self, default_instance, query_log_rows):
        check = _make_check(default_instance)
        row = query_log_rows[1]  # type=QueryFinish, duration=8500ms > 5000ms threshold
        payload = check._build_query_log_payload(row)

        assert payload['status'] == 'warning'
        assert payload['clickhouse.query_type'] == 'finish'
        assert payload['clickhouse.duration_ms'] == 8500

    def test_exception_query_is_error(self, default_instance, query_log_rows):
        check = _make_check(default_instance)
        row = query_log_rows[2]  # type=ExceptionWhileProcessing
        payload = check._build_query_log_payload(row)

        assert payload['status'] == 'error'
        assert payload['clickhouse.query_type'] == 'exception'
        assert payload['clickhouse.exception_code'] == 60
        assert 'nonexistent' in payload['clickhouse.exception']

    def test_exception_before_start_is_error(self, default_instance):
        check = _make_check(default_instance)
        row = {
            'cursor_us': 1743246012000000,
            'query_id': 'abc-before-start',
            'user': 'default',
            'query_duration_ms': 0,
            'memory_usage': 0,
            'read_rows': 0,
            'read_bytes': 0,
            'result_rows': 0,
            'written_rows': 0,
            'written_bytes': 0,
            'exception': 'Code: 62. DB::Exception: Syntax error',
            'exception_code': 62,
            'query': 'SELECTT 1',
            'type': 'ExceptionBeforeStart',
            'query_kind': 'Select',
            'current_database': 'default',
            'tables': '',
            'client_name': 'python-driver',
        }
        payload = check._build_query_log_payload(row)

        assert payload['status'] == 'error'
        assert payload['clickhouse.query_type'] == 'exception'
        assert payload['clickhouse.exception_code'] == 62

    def test_tags_are_joined(self, default_instance, query_log_rows):
        check = _make_check(default_instance)
        row = query_log_rows[0]
        payload = check._build_query_log_payload(row)

        assert payload['ddtags'] == 'env:test,clickhouse_cluster:test-cluster'

    def test_no_tags(self, default_instance, query_log_rows):
        default_instance['tags'] = []
        check = _make_check(default_instance)
        row = query_log_rows[0]
        payload = check._build_query_log_payload(row)

        assert payload['ddtags'] == ''

    def test_custom_cluster_name_sets_service(self, default_instance, query_log_rows):
        default_instance['cluster_name'] = 'analytics-prod'
        check = _make_check(default_instance)
        row = query_log_rows[0]
        payload = check._build_query_log_payload(row)

        assert payload['service'] == 'analytics-prod'

    def test_default_cluster_name_is_clickhouse(self, default_instance, query_log_rows):
        # No cluster_name in config -> defaults to "clickhouse"
        check = _make_check(default_instance)
        row = query_log_rows[0]
        payload = check._build_query_log_payload(row)

        assert payload['service'] == 'clickhouse'

    def test_missing_fields_use_defaults(self, default_instance):
        """Rows with missing optional fields should not crash."""
        check = _make_check(default_instance)
        sparse_row = {'cursor_us': 1000000000000000, 'type': 'QueryFinish'}
        payload = check._build_query_log_payload(sparse_row)

        assert payload['status'] == 'info'
        assert payload['message'] == ''
        assert payload['clickhouse.query_id'] == ''
        assert payload['clickhouse.duration_ms'] == 0
        assert payload['clickhouse.memory_bytes'] == 0
        assert payload['clickhouse.written_bytes'] == 0
        assert payload['clickhouse.query_kind'] == ''
        assert payload['clickhouse.database'] == ''


# ---------------------------------------------------------------------------
# Text log payload tests
# ---------------------------------------------------------------------------


class TestBuildTextLogPayload:
    def test_error_level(self, default_instance, text_log_rows):
        check = _make_check(default_instance)
        row = text_log_rows[0]  # Error
        payload = check._build_text_log_payload(row)

        assert payload['status'] == 'error'
        assert payload['ddsource'] == 'clickhouse'
        assert payload['clickhouse.logger'] == 'MergeTreeBackgroundExecutor'
        assert payload['clickhouse.query_id'] == 'abc-123-def-456'
        assert 'Memory limit exceeded' in payload['message']

    def test_warning_level(self, default_instance, text_log_rows):
        check = _make_check(default_instance)
        row = text_log_rows[1]  # Warning
        payload = check._build_text_log_payload(row)

        assert payload['status'] == 'warning'

    def test_fatal_level(self, default_instance, text_log_rows):
        check = _make_check(default_instance)
        row = text_log_rows[2]  # Fatal
        payload = check._build_text_log_payload(row)

        assert payload['status'] == 'critical'
        assert payload['clickhouse.thread_id'] == '1'

    def test_critical_level(self, default_instance):
        check = _make_check(default_instance)
        row = {
            'cursor_us': 1743246075000000,
            'level': 'Critical',
            'logger_name': 'Application',
            'message': 'Cannot allocate memory',
            'thread_id': 99,
            'query_id': '',
        }
        payload = check._build_text_log_payload(row)

        assert payload['status'] == 'critical'

    def test_query_id_empty_when_absent(self, default_instance):
        check = _make_check(default_instance)
        row = {
            'cursor_us': 1743246080000000,
            'level': 'Error',
            'logger_name': 'ServerErrorHandler',
            'message': 'Something failed',
            'thread_id': 5,
        }
        payload = check._build_text_log_payload(row)

        assert payload['clickhouse.query_id'] == ''

    def test_unknown_level_defaults_to_warning(self, default_instance):
        """Unknown log levels should map to 'warning' rather than crash."""
        check = _make_check(default_instance)
        row = {
            'cursor_us': 1000000000000000,
            'level': 'SomethingNew',
            'message': 'test',
        }
        payload = check._build_text_log_payload(row)

        assert payload['status'] == 'warning'

    def test_missing_level_defaults_to_warning(self, default_instance):
        check = _make_check(default_instance)
        row = {'cursor_us': 1000000000000000, 'message': 'no level key'}
        payload = check._build_text_log_payload(row)

        assert payload['status'] == 'warning'


# ---------------------------------------------------------------------------
# Cursor management tests
# ---------------------------------------------------------------------------


class TestCursorManagement:
    def test_get_cursor_returns_none_when_empty(self, default_instance):
        check = _make_check(default_instance)
        assert check._get_cursor('some_key') is None

    def test_set_and_get_cursor(self, default_instance):
        check = _make_check(default_instance)
        check._set_cursor('some_key', 1743246001000000)
        assert check._get_cursor('some_key') == 1743246001000000

    def test_default_cursor_is_reasonable(self, default_instance):
        check = _make_check(default_instance)
        cursor = check._default_cursor()
        now_us = int(time.time() * 1_000_000)
        backfill_us = 60 * 60 * 1_000_000  # 60 minutes

        # Should be within a few seconds of (now - 60 min)
        assert abs(cursor - (now_us - backfill_us)) < 5_000_000

    def test_extract_cursor_valid(self, default_instance, query_log_rows):
        check = _make_check(default_instance)
        result = check._extract_cursor(query_log_rows, 'test_source')
        assert result == 1743246010000000

    def test_extract_cursor_missing_field(self, default_instance):
        check = _make_check(default_instance)
        rows = [{'event_time': '2026-01-01'}]  # no cursor_us
        result = check._extract_cursor(rows, 'test_source')

        assert result is None
        assert check.log.warning.called

    def test_extract_cursor_empty_rows(self, default_instance):
        check = _make_check(default_instance)
        result = check._extract_cursor([], 'test_source')

        assert result is None
        assert check.log.warning.called

    def test_extract_cursor_unparseable(self, default_instance):
        check = _make_check(default_instance)
        rows = [{'cursor_us': 'not_a_number'}]
        result = check._extract_cursor(rows, 'test_source')

        assert result is None
        assert check.log.warning.called


# ---------------------------------------------------------------------------
# Timestamp tests
# ---------------------------------------------------------------------------


class TestTimestampSeconds:
    def test_valid_cursor_us(self, default_instance):
        check = _make_check(default_instance)
        row = {'cursor_us': 1743246001000000}
        ts = check._timestamp_seconds(row)
        assert ts == pytest.approx(1743246001.0)

    def test_missing_cursor_us_returns_zero(self, default_instance):
        check = _make_check(default_instance)
        row = {}
        ts = check._timestamp_seconds(row)
        assert ts == 0.0

    def test_corrupt_cursor_us_falls_back_with_warning(self, default_instance):
        check = _make_check(default_instance)
        row = {'cursor_us': 'corrupt'}
        ts = check._timestamp_seconds(row)

        # Should fall back to current time
        assert abs(ts - time.time()) < 5
        assert check.log.warning.called


# ---------------------------------------------------------------------------
# HTTP layer tests (_query_clickhouse)
# ---------------------------------------------------------------------------


class TestQueryClickhouse:
    def test_sends_correct_request(self, default_instance):
        check = _make_check(default_instance)
        mock_resp = _mock_query_response([{'col': 'val'}])

        with patch.object(check._session, 'post', return_value=mock_resp) as mock_post:
            rows = check._query_clickhouse('SELECT 1')

        mock_post.assert_called_once_with(
            'https://queries.clickhouse.cloud/service/test-service-uuid/run',
            params={'format': 'JSONEachRow'},
            json={'sql': 'SELECT 1'},
            timeout=30,
        )
        assert rows == [{'col': 'val'}]

    def test_empty_response(self, default_instance):
        check = _make_check(default_instance)
        mock_resp = MagicMock()
        mock_resp.text = ''
        mock_resp.raise_for_status = MagicMock()

        with patch.object(check._session, 'post', return_value=mock_resp):
            rows = check._query_clickhouse('SELECT 1')

        assert rows == []

    def test_http_error_raises(self, default_instance):
        check = _make_check(default_instance)

        with (
            patch.object(
                check._session,
                'post',
                side_effect=requests.exceptions.HTTPError('500 Server Error'),
            ),
            pytest.raises(requests.exceptions.HTTPError),
        ):
            check._query_clickhouse('SELECT 1')

    def test_connection_error_raises(self, default_instance):
        check = _make_check(default_instance)

        with (
            patch.object(
                check._session,
                'post',
                side_effect=requests.exceptions.ConnectionError('DNS failed'),
            ),
            pytest.raises(requests.exceptions.ConnectionError),
        ):
            check._query_clickhouse('SELECT 1')

    def test_multiline_json_each_row_parsed(self, default_instance):
        check = _make_check(default_instance)
        mock_resp = MagicMock()
        mock_resp.text = '{"a":1}\n{"a":2}\n{"a":3}\n'
        mock_resp.raise_for_status = MagicMock()

        with patch.object(check._session, 'post', return_value=mock_resp):
            rows = check._query_clickhouse('SELECT a FROM t')

        assert rows == [{'a': 1}, {'a': 2}, {'a': 3}]

    def test_custom_timeout_used(self, default_instance):
        default_instance['query_timeout_seconds'] = 90
        check = _make_check(default_instance)
        mock_resp = _mock_query_response([])

        with patch.object(check._session, 'post', return_value=mock_resp) as mock_post:
            check._query_clickhouse('SELECT 1')

        _, kwargs = mock_post.call_args
        assert kwargs['timeout'] == 90


# ---------------------------------------------------------------------------
# Full collection flow tests
# ---------------------------------------------------------------------------


class TestCollectQueryLogs:
    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_sends_logs_and_updates_cursor(self, mock_query, default_instance, query_log_rows):
        check = _make_check(default_instance)
        mock_query.return_value = query_log_rows

        check._collect_query_logs()

        # Should send 3 log entries
        assert len(check._sent_logs) == 3

        # Cursor should be set to the last row's timestamp
        cursor = check._get_cursor('clickhouse_cloud.cursor.query_log')
        assert cursor == 1743246010000000

        # Service check should report OK
        assert (SC_QUERY_LOG_CONNECT, ClickHouseCloudCheck.OK) in check._service_checks

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_no_rows_does_not_update_cursor(self, mock_query, default_instance):
        check = _make_check(default_instance)
        mock_query.return_value = []

        check._collect_query_logs()

        assert len(check._sent_logs) == 0
        assert check._get_cursor('clickhouse_cloud.cursor.query_log') is None

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_query_failure_reports_critical(self, mock_query, default_instance):
        check = _make_check(default_instance)
        mock_query.side_effect = Exception('Connection refused')

        check._collect_query_logs()

        assert (SC_QUERY_LOG_CONNECT, ClickHouseCloudCheck.CRITICAL) in check._service_checks
        assert len(check._sent_logs) == 0

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_no_send_log_method_does_not_crash(self, mock_query, default_instance, query_log_rows):
        check = _make_check(default_instance)
        mock_query.return_value = query_log_rows[:1]

        # Simulate older AgentCheck implementations that don't expose send_log.
        check.send_log = None

        check._collect_query_logs()

        assert check.log.info.called

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_partial_emit_failure_still_advances_cursor(self, mock_query, default_instance, query_log_rows):
        """If _emit_log fails for some rows, the cursor should still advance."""
        check = _make_check(default_instance)
        mock_query.return_value = query_log_rows

        call_count = 0
        original_emit = check._emit_log

        def _flaky_emit(entry):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError('Transient send_log failure')
            original_emit(entry)

        check._emit_log = _flaky_emit
        check._collect_query_logs()

        # 2 of 3 logs should have been sent (the 2nd failed)
        assert len(check._sent_logs) == 2
        # Cursor should still advance to last row
        cursor = check._get_cursor('clickhouse_cloud.cursor.query_log')
        assert cursor == 1743246010000000

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_missing_cursor_us_does_not_advance(self, mock_query, default_instance):
        """If the last row has no cursor_us, cursor should not advance."""
        check = _make_check(default_instance)
        rows = [{'type': 'QueryFinish', 'query': 'SELECT 1'}]  # no cursor_us
        mock_query.return_value = rows

        check._collect_query_logs()

        assert check._get_cursor('clickhouse_cloud.cursor.query_log') is None
        assert check.log.warning.called

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_gauge_reports_row_count(self, mock_query, default_instance, query_log_rows):
        check = _make_check(default_instance)
        mock_query.return_value = query_log_rows

        check._collect_query_logs()

        assert (GAUGE_QUERY_LOG_ROWS, 3) in check._gauges


class TestCollectTextLogs:
    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_sends_logs_and_updates_cursor(self, mock_query, default_instance, text_log_rows):
        check = _make_check(default_instance)
        mock_query.return_value = text_log_rows

        check._collect_text_logs()

        assert len(check._sent_logs) == 3

        cursor = check._get_cursor('clickhouse_cloud.cursor.text_log')
        assert cursor == 1743246070000000

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_query_failure_reports_critical(self, mock_query, default_instance):
        check = _make_check(default_instance)
        mock_query.side_effect = Exception('Timeout')

        check._collect_text_logs()

        assert (SC_TEXT_LOG_CONNECT, ClickHouseCloudCheck.CRITICAL) in check._service_checks

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_gauge_reports_row_count(self, mock_query, default_instance, text_log_rows):
        check = _make_check(default_instance)
        mock_query.return_value = text_log_rows

        check._collect_text_logs()

        assert (GAUGE_TEXT_LOG_ROWS, 3) in check._gauges


# ---------------------------------------------------------------------------
# Entry point tests
# ---------------------------------------------------------------------------


class TestCheckEntryPoint:
    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_check_calls_both_collectors(self, mock_query, default_instance, query_log_rows, text_log_rows):
        check = _make_check(default_instance)
        # First call returns query logs, second returns text logs
        mock_query.side_effect = [query_log_rows, text_log_rows]

        check.check(default_instance)

        # All logs from both sources
        assert len(check._sent_logs) == 6

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_check_respects_disabled_collectors(self, mock_query, default_instance):
        default_instance['collect_query_logs'] = False
        default_instance['collect_text_logs'] = False
        check = _make_check(default_instance)

        check.check(default_instance)

        mock_query.assert_not_called()

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_cursor_persists_across_runs(self, mock_query, default_instance, query_log_rows):
        check = _make_check(default_instance)
        default_instance['collect_text_logs'] = False
        check.collect_text_logs = False

        # First run
        mock_query.return_value = query_log_rows
        check.check(default_instance)
        first_cursor = check._get_cursor('clickhouse_cloud.cursor.query_log')

        # Second run with no new data
        mock_query.return_value = []
        check.check(default_instance)
        second_cursor = check._get_cursor('clickhouse_cloud.cursor.query_log')

        # Cursor should not change on empty run
        assert first_cursor == second_cursor == 1743246010000000


# ---------------------------------------------------------------------------
# Retry adapter tests
# ---------------------------------------------------------------------------


class TestRetryConfiguration:
    def test_session_has_retry_adapter(self, default_instance):
        check = _make_check(default_instance)
        adapter = check._session.get_adapter('https://example.com')
        assert isinstance(adapter, requests.adapters.HTTPAdapter)
        assert adapter.max_retries.total == 2
        assert adapter.max_retries.status_forcelist == [502, 503, 504]

    def test_session_auth_configured(self, default_instance):
        check = _make_check(default_instance)
        assert check._session.auth == ('test-key-id', 'test-key-secret')


# ---------------------------------------------------------------------------
# Noise filter tests
# ---------------------------------------------------------------------------


class TestInternalUserFilter:
    """Tests for the exclude_internal_users query_log filter."""

    def test_exclude_internal_users_default_is_true(self, default_instance):
        check = _make_check(default_instance)
        assert check.exclude_internal_users is True

    def test_exclude_internal_users_explicit_false(self, default_instance):
        default_instance['exclude_internal_users'] = False
        check = _make_check(default_instance)
        assert check.exclude_internal_users is False

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_internal_user_filter_injected_by_default(self, mock_query, default_instance, query_log_rows):
        """When exclude_internal_users is True (default), the SQL should contain
        the internal user filter clause."""
        check = _make_check(default_instance)
        mock_query.return_value = query_log_rows

        check._collect_query_logs()

        sql_sent = mock_query.call_args[0][0]
        assert '%-internal' in sql_sent
        assert 'clickhouse-cloud-%' in sql_sent
        assert 'prometheus-exporter' in sql_sent

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_internal_user_filter_omitted_when_disabled(self, mock_query, default_instance, query_log_rows):
        """When exclude_internal_users is False, the SQL should NOT contain
        the internal user filter clause."""
        default_instance['exclude_internal_users'] = False
        check = _make_check(default_instance)
        mock_query.return_value = query_log_rows

        check._collect_query_logs()

        sql_sent = mock_query.call_args[0][0]
        assert '%-internal' not in sql_sent
        assert 'clickhouse-cloud-%' not in sql_sent
        assert 'prometheus-exporter' not in sql_sent

    def test_internal_user_filter_constant_syntax(self):
        """The INTERNAL_USER_FILTER constant should be valid SQL fragments."""
        assert 'NOT LIKE' in INTERNAL_USER_FILTER
        assert '%-internal' in INTERNAL_USER_FILTER
        assert 'clickhouse-cloud-%' in INTERNAL_USER_FILTER
        assert 'prometheus-exporter' in INTERNAL_USER_FILTER
        assert "user != ''" in INTERNAL_USER_FILTER


class TestQueryProfilerFilter:
    """Tests for the text_log QueryProfiler/GlobalProfiler noise filter."""

    def test_text_log_sql_excludes_query_profiler(self):
        """TEXT_LOG_SQL should filter out QueryProfiler logger entries."""
        assert 'QueryProfiler' in TEXT_LOG_SQL
        assert 'GlobalProfiler' in TEXT_LOG_SQL
        assert 'NOT IN' in TEXT_LOG_SQL

    @patch('datadog_checks.clickhouse_cloud.check.ClickHouseCloudCheck._query_clickhouse')
    def test_profiler_rows_not_fetched(self, mock_query, default_instance):
        """Rows from QueryProfiler/GlobalProfiler loggers should be excluded
        at the SQL level -- they should never appear in results."""
        check = _make_check(default_instance)
        # Simulate ClickHouse returning only non-profiler rows (as it should
        # with the filter in place)
        mock_query.return_value = []

        check._collect_text_logs()

        sql_sent = mock_query.call_args[0][0]
        assert 'QueryProfiler' in sql_sent
        assert 'GlobalProfiler' in sql_sent
