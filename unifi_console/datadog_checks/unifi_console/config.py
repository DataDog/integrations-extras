from datadog_checks.base import ConfigurationError


class UnifiConfig(object):
    def __init__(self, instance, init_config, log) -> None:
        self.log = log

        # Use self.instance to read the check configuration
        self.url = instance.get("url", "")
        self.user = instance.get("user", "")
        self.password = instance.get("pwd", "")
        self.site = instance.get("site", "default")
        self.tags = ["url:{}".format(self.url), "site:{}".format(self.site)] + instance.get("tags", [])

        self.validate_config()

    def validate_config(self):
        if not self.url:
            raise ConfigurationError("Missing configuration: url")
        if not self.user:
            raise ConfigurationError("Missing configuration: user")
        if not self.password:
            raise ConfigurationError("Missing configuration: pwd")
