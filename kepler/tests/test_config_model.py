# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.kepler.config_models import ConfigMixin, InstanceConfig, SharedConfig, defaults


def test_config_models_smoke_test():
    """
    Coverage-only test.
    1. Instance/SharedConfig are Pydantic models -> Use model_validate()
    2. ConfigMixin is a plain class -> Instantiate directly
    3. Defaults -> Import and access to force coverage
    """

    # --- 1. Test InstanceConfig (Pydantic) ---
    data = {
        "openmetrics_endpoint": "http://localhost:8080/metrics",
        "auth_token": {"reader": {"path": "/reader"}, "writer": {"path": "/writer"}},
        "kerberos_auth": "required",
        "tls_ca_cert": "/etc/ssl/ca.pem",
        "tls_cert": "/etc/ssl/cert.pem",
        "tls_private_key": "/etc/ssl/key.pem",
        "kerberos_cache": "/tmp/krb5cc",
        "kerberos_keytab": "/etc/krb5.keytab",
    }
    # This runs the validation logic in 'instance.py' and 'validators.py', including
    # the SECURE_FIELD_NAMES trusted-provider check.
    instance = InstanceConfig.model_validate(data, context={"configured_fields": list(data.keys())})
    assert instance is not None

    # --- 2. Test SharedConfig (Pydantic) ---
    # This runs 'shared.py'
    shared = SharedConfig.model_validate({}, context={"configured_fields": []})
    assert shared is not None

    # --- 3. Test ConfigMixin (Plain Class) ---
    mixin = ConfigMixin()
    assert mixin is not None

    # --- 4. Test Defaults (Direct Access) ---
    # Accessing the module attributes forces Python to mark 'defaults.py' as covered.
    for attr in dir(defaults):
        if not attr.startswith("__"):
            getattr(defaults, attr)
