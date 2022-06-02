# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.nn_sdwan import NnSdwanCheck


@pytest.mark.unit
def test_empty_instance(aggregator, instance_empty):
    with pytest.raises(ConfigurationError):
        NnSdwanCheck('nn_sdwan', {}, [instance_empty])


@pytest.mark.unit
def test_missing_hostname(aggregator, instance_missing_hostname):
    with pytest.raises(ConfigurationError):
        NnSdwanCheck('nn_sdwan', {}, [instance_missing_hostname])


@pytest.mark.unit
def test_missing_username(aggregator, instance_missing_username):
    with pytest.raises(ConfigurationError):
        NnSdwanCheck('nn_sdwan', {}, [instance_missing_username])


@pytest.mark.unit
def test_missing_password(aggregator, instance_missing_password):
    with pytest.raises(ConfigurationError):
        NnSdwanCheck('nn_sdwan', {}, [instance_missing_password])


@pytest.mark.unit
def test_missing_protocol(aggregator, instance_missing_protocol):
    with pytest.raises(ConfigurationError):
        NnSdwanCheck('nn_sdwan', {}, [instance_missing_protocol])


@pytest.mark.unit
def test_normal_instance(aggregator, instance_normal):
    NnSdwanCheck('nn_sdwan', {}, [instance_normal])


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_metrics_received(aggregator, instance_normal):
    check = NnSdwanCheck('nn_sdwan', {}, [instance_normal])

    check.check(instance_normal)
    # for metric in ALL_METRICS:
    #     aggregator.assert_metric(metric, at_least=0)

    # aggregator.assert_all_metrics_covered()
    # aggregator.assert_metrics_using_metadata(get_metadata_metrics())
