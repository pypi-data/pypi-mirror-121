# Changelog

## 21.8.0 (2021-09-03)

* Fix `klio job verify --create-resources` to properly run Spotify specific commands even after general verification failures

## 21.2.0 (2021-03-16)

* Version sync with `klio-cli`

## 0.2.1 (2020-12-11)

* Updates from moving `with_klio_config` to klio core
* Dropped support for Python 3.5 (reached its [end-of-life support](https://www.python.org/downloads/release/python-3510/))

## 0.2.0 (2020-10-06)

Initial general release for v2 of `spotify-klio-cli` (no change since `0.2.0.alpha1`).

## 0.2.0.alpha1 (2020-09-02)

### Added

* New command, `klio job convert-v1-config`, to convert Klio v1 configuration to v2.

## 0.1.0 (2020-08-12)

Final minor release of v1 for `spotify-klio-cli` (no change since `0.0.10`).

## 0.0.10 (2020-06-29)

### Fixed

* Fixed typo in track max length CLI option

## 0.0.9 (2020-05-04)

### Changed

* Tingle verification will attempt to add access if `--create-resources` is true in `klio job verify` (functionality was previously in klio-cli)

## 0.0.8 (2020-04-08)

* Moved tingle verification from `klio-cli` into `spotify-klio-cli`.

## 0.0.7 (2020-04-06)

### Fixed

* Update imports to reflect directory structure changes in `klio-cli`.

## 0.0.6 (2020-03-31)

* Update `spotify-klio-runner` to `spotify-klio-exec` when checking for internal dependencies.

## 0.0.5 (2020-03-27)

* Redirect users to Backstage when trying to create a new Klio job.

## 0.0.4 (2020-03-26)

### Added

* Add generate-entities subcommand to the profile command generate test messages using BigQuery.

## 0.0.3 (2020-03-24)

### Fixed

* Incorporated [abstraction changes](https://ghe.spotify.net/sigint/klio/pull/86/commits/3583215c1cc219c2ea3b6dea206cd7e87baacb68) made in `klio-cli`.

## 0.0.2 (2020-03-03)

### Added

* Add support for running/maintaining a job with multiple configuration files.

## 0.0.1 (2020-01-15)

Initial Release!

### Added

* Option to run jobs with or without XPN
* Check if job has `spotify-klio-runner` installed
