import pytest
from unittest import mock
from datadog_checks.stonebranch import StonebranchCheck


@pytest.mark.unit
def test_check(dd_run_check, aggregator, instance):
    check = StonebranchCheck('stonebranch', {}, [instance])

    # Mock all the methods that make external calls
    with mock.patch.object(check, '_check_api_connectivity') as mock_api:

        # Make API check succeed and emit a test metric
        def mock_api_call():
            check.gauge('stonebranch.api.available', 1)

        mock_api.side_effect = mock_api_call

        dd_run_check(check)
    
    # Check that the API availability metric was submitted
    aggregator.assert_metric('stonebranch.stonebranch.api.available', value=1)
    
    # Check service check is OK
    aggregator.assert_service_check('stonebranch.stonebranch_uc.can_connect', check.OK)


@pytest.mark.unit  
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    check = StonebranchCheck('stonebranch', {}, [instance])

    # Mock API check to fail
    with mock.patch.object(check, '_check_api_connectivity') as mock_api:

        mock_api.side_effect = Exception("Connection failed")

        # Expect the check to raise an exception
        with pytest.raises(Exception):
            dd_run_check(check)
    
    # Check service check shows critical
    aggregator.assert_service_check('stonebranch.stonebranch_uc.can_connect', check.CRITICAL)