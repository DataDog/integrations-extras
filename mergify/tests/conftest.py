# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import pytest

if "MERGIFY_TOKEN" in os.environ:

    @pytest.fixture(scope="session")
    def dd_environment():
        yield {
            "token": os.environ["MERGIFY_TOKEN"],
            "repositories": {
                os.getenv("MERGIFY_REPOSITORY", "Mergifyio/mergify"): [os.getenv("MERGIFY_BRANCH", "main")]
            },
        }


@pytest.fixture
def instance():
    return {
        "repositories": {"owner/repository": ["main"]},
        "token": "a_token",
        "tags": ["test:mergify"],
    }
