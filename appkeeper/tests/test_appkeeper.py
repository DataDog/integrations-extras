import pytest
from datadog_checks.appkeeper import AppKeeperCheck
from datadog_checks.base import ConfigurationError
from datadog_checks.base.errors import CheckException

@pytest.mark.unit
def test_config():
    c = AppKeeperCheck()

    # 空のインスタンス
    # with pytest.raises(ConfigurationError):
    #     instance = {}
    #     c.check(instance)

    instance = {'account': 'xxxx', 'integrationToken': '000000'}
    x = c.check(instance=instance)
    print(x)
    assert(x == 0)
