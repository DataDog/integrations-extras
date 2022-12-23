EXPECTED_CHECKS = [
    'filemage.services_up',
    'filemage.metrics_up',
]

MOCK_INSTANCE_GOOD = {
    "filemage_service_checks": ["postgres", "gateway"],
    "filemage_api_config": {"rooturl": "https://localhost/", "apitoken": "secret", "verifyssl": False},
}

MOCK_INSTANCE_BAD = {}
