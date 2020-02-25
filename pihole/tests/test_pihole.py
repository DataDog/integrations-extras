import pytest
from datadog_checks.pihole import PiholeCheck
from datadog_checks.base import ConfigurationError


@pytest.mark.unit
def test_config():
    instance = {}
    c = PiholeCheck('pihole', {}, [instance])

    # empty should fail
    with pytest.raises(ConfigurationError):
        c.check(instance)

# Testing integration status check using docker
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = PiholeCheck('pihole', {}, [instance])

    c.check(instance)
    aggregator.assert_service_check('pihole.running', PiholeCheck.OK)


# Testing known metric value using docker
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment')
def test_domains_being_blocked(aggregator, instance):
    c = PiholeCheck('pihole', {}, [instance])

    c.check(instance)
    aggregator.assert_metric(name="pihole.domains_being_blocked", value=125247.0)

# Testing known metric value using docker
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment')
def test_unique_clients(aggregator, instance):
    c = PiholeCheck('pihole', {}, [instance])

    c.check(instance)
    aggregator.assert_metric(name="pihole.unique_clients", value=1)

# Testing known metric value using docker
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment')
def test_clients_ever_seen(aggregator, instance):
    c = PiholeCheck('pihole', {}, [instance])

    c.check(instance)
    aggregator.assert_metric(name="pihole.clients_ever_seen", value=1)# Testing known metric value using docker
