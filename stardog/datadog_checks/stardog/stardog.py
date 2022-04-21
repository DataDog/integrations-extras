import re

from datadog_checks.base import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = "stardog"


def convert_query_speed(in_key, in_val):
    try:
        if in_val["duration_units"] != "seconds":
            raise Exception("Unsupported duration units")
        if in_val["rate_units"] != "calls/second":
            raise Exception("Unsupported rate units")
    except KeyError:
        raise Exception("The units are not properly defined")

    entry_key = [
        "count",
        "max",
        "mean",
        "min",
        "p50",
        "p75",
        "p95",
        "p98",
        "p99",
        "p999",
        "stddev",
        "m15_rate",
        "m1_rate",
        "m5_rate",
        "mean_rate",
    ]
    out_dict = {}
    for ent in entry_key:
        new_key = "stardog.%s.%s" % (in_key, ent)
        out_dict[new_key] = in_val[ent]
    return out_dict


def convert_query_counts(in_key, in_val):
    entry_key = [
        "count",
        "max",
        "mean",
        "min",
        "p50",
        "p75",
        "p95",
        "p98",
        "p99",
        "p999",
        "stddev",
    ]
    out_dict = {}
    for ent in entry_key:
        new_key = "stardog.%s.%s" % (in_key, ent)
        out_dict[new_key] = in_val[ent]
    return out_dict


def convert_default(in_key, in_val):
    if "stddev" in in_val:
        if "duration_units" in in_val:
            return convert_query_speed(in_key, in_val)
        return convert_query_counts(in_key, in_val)

    try:
        key = "stardog.%s" % in_key
        val = float(in_val["value"] if "value" in in_val else in_val["count"])
        return {key: val}
    except:
        return None


def convert_default_db(in_key, in_val, db_name):
    # key = in_key.replace("%s." % db_name, "")
    return convert_default(in_key, in_val)


class StardogCheck(AgentCheck):
    def _process_doc(self, doc, tags, add_db_tags=False):
        db_regex = re.compile(r"(databases|kga)\.([^\.]+)\..*")
        for k in doc:
            local_tags = tags[:]
            db_match = db_regex.match(k)
            if db_match is not None:
                try:
                    db_name = db_match.group(2)
                    if add_db_tags:
                        local_tags.append("database:%s" % db_name)
                except Exception:
                    self.log.warning("No database name was found")
                    continue

            values_map = convert_default(k, doc[k])
            if values_map is not None:
                for report_key in values_map:
                    self.log.debug(
                        "Sending %s=%s to Datadog",
                        report_key,
                        values_map[report_key],
                    )

                    self.gauge(report_key, values_map[report_key], tags=local_tags)
            else:
                self.log.warning("No values map: %s and %s", k, doc[k])

    def check(self, _):
        try:
            response = self.http.get(self.instance["stardog_url"] + "/admin/status")
        except KeyError:
            raise Exception("The Stardog check instance is not properly configured")

        if response.status_code != 200:
            response.raise_for_status()
        json_doc = response.json()
        try:
            tags = self.instance["tags"]
            if type(tags) != list:
                self.log.warning("The tags list in the Stardog check is not configured properly")
                tags = []
        except KeyError:
            tags = []

        tags.append("stardog_url:%s" % self.instance["stardog_url"])
        self._process_doc(json_doc, tags)
