# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from datetime import datetime, timedelta
from time import mktime

NOW = datetime.utcnow()
NINE_DAYS_AGO = mktime((NOW - timedelta(days=9)).timetuple())
SIXTEEN_DAYS_AGO = mktime((NOW - timedelta(days=16)).timetuple())
