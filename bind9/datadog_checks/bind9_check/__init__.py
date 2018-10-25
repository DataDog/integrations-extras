# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from .bind9_check import bind9_check
from .__about__ import __version__

__all__ = [
    '__version__',
    'bind9_check'
]
