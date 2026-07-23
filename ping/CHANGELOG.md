# CHANGELOG - Ping

## 1.0.3 / 2026-07-23

***Fixed***:

* Fix the Ping check on non-English Windows. It no longer crashes on localized output (``'utf-8' codec can't decode byte 0x81``) and no longer reports reachable hosts as down. The check now uses the UTF-8 code page and matches ping's untranslated ``ms`` unit instead of the localized "time" label ([#3075](https://github.com/DataDog/integrations-extras/pull/3075)).

## 1.0.2 / 2021-09-30

***Fixed***:

* Fix compatibility with non-US Windows ([#992](https://github.com/DataDog/integrations-extras/pull/992))

## 1.0.1 / 2021-03-04

***Fixed***:

* Fix ping check with bad float conversion ([#818](https://github.com/DataDog/integrations-extras/pull/818))
