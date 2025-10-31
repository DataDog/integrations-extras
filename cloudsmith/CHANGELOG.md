# CHANGELOG - Cloudsmith


## 0.0.3 / 2025-10-29
### Added
* Dashboard: Historical (time series + bar) visualization widgets for daily storage and bandwidth quota percentages to support day-over-day tracking while retaining existing query value widgets.
* Real-time bandwidth interval bytes metric (`cloudsmith.bandwidth_bytes_interval`) via Cloudsmith v2 analytics endpoint (disabled by default; enable with `enable_realtime_bandwidth: true`). Uses fixed internal defaults (minute interval, aggregate `BYTES_DOWNLOADED_SUM`, look-back 120m, refresh 300s, min points 2) to keep configuration simple.
* Dashboard widget for realtime interval bytes.

### Documentation
* Clarified quota-based metric update cadence (daily) and recommended historical visualization widgets.

### Internal
* Realtime implementation uses per-instance state (no module-level globals) for reliability across Agent restarts.
* Tests updated for analytics response shape and realtime emission / suppression on insufficient points.
* Style fixes (line length, indentation) in `check.py`.

