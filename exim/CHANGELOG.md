# CHANGELOG - exim

## 1.1.0 / 2026-10-09

***Fixed***:

* Fix metrics collection: `exim -bp | exiqsumm` was passed to `get_subprocess_output` as a single argv without a shell, so the command never ran and the check reported no metrics while the service check stayed `OK`. The pipeline now runs through `/bin/sh`, and a failing `exim -bp` is no longer masked by a successful `exiqsumm` run. ([#3208](https://github.com/DataDog/integrations-extras/pull/3208))
* Report `exim.returns.output` as `CRITICAL` with the command's stderr when the command exits with a non-zero status or prints no output, and log the failure at warning level. ([#3208](https://github.com/DataDog/integrations-extras/pull/3208))
* Convert `KB` and `MB` volumes using 1024-based units, matching how `exiqsumm` rounds them. ([#3208](https://github.com/DataDog/integrations-extras/pull/3208))

***Added***:

* Add the `exim_path`, `exiqsumm_path` and `use_sudo` instance options. `use_sudo` runs `exim -bp` through `sudo -n` for installations where `queue_list_requires_admin` is enabled. ([#3208](https://github.com/DataDog/integrations-extras/pull/3208))

## 1.0.0

***Added***:

* Initial release with metrics and service check integration.
