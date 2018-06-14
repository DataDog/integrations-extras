# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from __future__ import print_function, unicode_literals

import os

# the root of the repo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Note: these are the names of the folder containing the check
AGENT_BASED_INTEGRATIONS = [
]

# If a file changes in a PR with any of these file extensiosn, a test will run against the check containing the file
TESTABLE_FILE_EXTENSIONS = (
    '.py',
    '.ini',
    '.txt',
)
