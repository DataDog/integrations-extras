# (C) voseghale 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_DIR = os.path.join(HERE, 'fixtures')


def fixture_path(name):
    return os.path.join(FIXTURE_DIR, name)


def read_fixture(name):
    with open(fixture_path(name), 'r') as f:
        return f.read()
