# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from os import utime


def touch(fname, times=None):
    with open(fname, 'a'):
        utime(fname, times)

    return fname
