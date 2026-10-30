#!/usr/bin/env python3
"""Create the Datadog incident type and property fields used by the Cyberhaven workflow.

Creates the "Cyberhaven Incident" incident type and its property fields when they do not exist, reuses
them when they do, and prints the incident type UUID.

Environment: DD_API_KEY, DD_APP_KEY and DD_SITE (default datadoghq.com). The application key's owner
needs the Incident Settings Write and Incident Read permissions.

Usage: python3 setup_datadog_incident_type.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

TYPE_NAME = "Cyberhaven Incident"
TYPE_PREFIX = "CH"
TYPE_DESCRIPTION = "Cyberhaven incidents synced from Cyberhaven logs"

TEXTBOX = 3
MAX_ATTEMPTS = 4
PAGE_SIZE = 1000

# (name, display name, category). All fields are text so new Cyberhaven values never break the schema.
FIELDS = [
    ("source_incident_id", "Cyberhaven Incident ID", None),
    ("cyberhaven_incident_url", "Cyberhaven Incident URL", None),
    ("tenant", "Tenant", None),
    ("policy_name", "Policy Name", "what_happened"),
    ("policy_severity", "Policy Severity", None),
    ("ai_severity", "AI Severity", None),
    ("cyberhaven_created_by", "Created By", None),
    ("dataset_name", "Dataset Name", None),
    ("dataset_sensitivity", "Dataset Sensitivity", None),
    ("risk_score", "Risk Score", None),
    ("blocked", "Blocked", None),
    ("user", "User", "what_happened"),
    ("user_id", "User ID", None),
    ("action_kind", "Action", "what_happened"),
    ("hostname", "Hostname", "what_happened"),
    ("device_type", "Device Type", None),
    ("sensor_kind", "Sensor Kind", None),
    ("client_ip", "Client IP", None),
    ("data_size_bytes", "Data Size (bytes)", None),
    ("warning_status", "Warning Status", None),
    ("event_time", "Event Time", None),
    ("trigger_time", "Trigger Time", None),
    ("resolution_time", "Resolution Time", "why_it_happened"),
    ("close_reason", "Close Reason", "why_it_happened"),
    ("close_note", "Close Note", "why_it_happened"),
    ("cyberhaven_status", "Cyberhaven Status", None),
    ("cyberhaven_ai_summary", "AI Summary", "what_happened"),
    ("policy_id", "Policy ID", None),
    ("dataset_id", "Dataset ID", None),
    ("last_change", "Last Change", "what_happened"),
]


class ApiError(Exception):
    def __init__(self, method, path, status, detail):
        super().__init__(f"{method} {path} -> {status}: {detail}")
        self.status = status


def normalize_site(site):
    site = site.strip().lower().split("://", 1)[-1].strip("/")
    for prefix in ("api.", "app."):
        if site.startswith(prefix):
            site = site[len(prefix):]
    return site


def call(method, path, body=None, query=None):
    url = f"https://api.{SITE}{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": os.environ["DD_API_KEY"],
        "DD-APPLICATION-KEY": os.environ["DD_APP_KEY"],
    }
    for attempt in range(1, MAX_ATTEMPTS + 1):
        delay = min(2 ** attempt, 30)
        try:
            req = urllib.request.Request(url, data=data, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            if (e.code != 429 and e.code < 500) or attempt == MAX_ATTEMPTS:
                raise ApiError(method, path, e.code, detail)
            retry_after = e.headers.get("Retry-After", "")
            if retry_after.isdigit():
                delay = min(int(retry_after), 60)
        except (urllib.error.URLError, OSError, ValueError) as e:
            if attempt == MAX_ATTEMPTS:
                raise ApiError(method, path, None, str(e))
        time.sleep(delay)


def find_type_id():
    out = call("GET", "/api/v2/incidents/config/types")
    for t in out.get("data", []):
        if t.get("attributes", {}).get("name") == TYPE_NAME:
            return t["id"]
    return None


def create_type():
    body = {"data": {"type": "incident_types", "attributes": {
        "name": TYPE_NAME, "description": TYPE_DESCRIPTION, "prefix": TYPE_PREFIX}}}
    return call("POST", "/api/v2/incidents/config/types", body)["data"]["id"]


def field_names(type_id):
    names, page = set(), 0
    while True:
        out = call("GET", "/api/v2/incidents/config/user-defined-fields", query={
            "filter[incident-type]": type_id, "page[size]": PAGE_SIZE, "page[number]": page})
        rows = out.get("data", [])
        for row in rows:
            owner = row.get("relationships", {}).get("incident_type", {}).get("data", {}).get("id")
            if owner in (None, type_id):
                names.add(row.get("attributes", {}).get("name"))
        if len(rows) < PAGE_SIZE:
            return names
        page += 1


def create_field(type_id, name, display, category):
    attributes = {"name": name, "type": TEXTBOX, "display_name": display}
    if category:
        attributes["category"] = category
    body = {"data": {
        "type": "user_defined_field",
        "attributes": attributes,
        "relationships": {"incident_type": {"data": {"id": type_id, "type": "incident_types"}}},
    }}
    call("POST", "/api/v2/incidents/config/user-defined-fields", body)


def fail_api(e):
    if e.status in (401, 403):
        sys.exit(f"not authorized: {e}\nThe application key's owner needs the Incident Settings Write and "
                 "Incident Read permissions, and DD_SITE must match your Datadog site.")
    sys.exit(f"failed: {e}")


def main():
    if not (os.environ.get("DD_API_KEY") and os.environ.get("DD_APP_KEY")):
        sys.exit("Set DD_API_KEY and DD_APP_KEY.")

    try:
        type_id = find_type_id()
        if type_id:
            print(f"incident type '{TYPE_NAME}' exists: {type_id}")
        else:
            type_id = create_type()
            print(f"created incident type '{TYPE_NAME}': {type_id}")

        existing = field_names(type_id)
        for name, display, category in FIELDS:
            if name in existing:
                continue
            create_field(type_id, name, display, category)
            print(f"created field {name}")

        missing = [name for name, _, _ in FIELDS if name not in field_names(type_id)]
    except ApiError as e:
        fail_api(e)

    if missing:
        sys.exit(f"{len(missing)} of {len(FIELDS)} fields are missing on incident type {type_id}: "
                 + ", ".join(missing))
    print(f"verified: all {len(FIELDS)} fields are present")
    print(f"incident_type_uuid = {type_id}")


SITE = normalize_site(os.environ.get("DD_SITE", "datadoghq.com"))

if __name__ == "__main__":
    main()
