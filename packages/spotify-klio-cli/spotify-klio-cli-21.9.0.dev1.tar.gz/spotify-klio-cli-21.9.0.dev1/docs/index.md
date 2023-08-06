# `spotify-klio-cli`

Internal plugins for the [`klio-cli`](https://klio.readthedocs.io/en/latest/reference/cli/index.html) tool.

## Changes in `klio` Subcommands

The following subcommands have supplementary behavior to those in [`klio-cli`](https://klio.readthedocs.io/en/latest/reference/cli/index.html).

### `klio job run`

The `klio job run` command has an **additional flag**, `--xpn`/`--no-xpn`, to make use of the internal XPN network in GCP.  By default, `--xpn` is used.

### `klio job verify`

When using the `--create-resources` flag in `klio job verify`, `spotify-klio-cli` will ensure Tingle has access to deploy the Klio job, in addition to creating the needed GCP resources that happens with `klio-cli`.

### `klio job create`

Unlike `klio-cli`, the `spotify-klio-cli` **will not allow** users to create a Klio job via `klio job create`. The proper way to create a Klio job is through [Backstage](https://backstage.spotify.net/create-component/klio-streaming-skeleton).


## Additional Subcommands

The following subcommands are only available with `spotify-klio-cli` and not found in `klio-cli`.

### `klio job convert-v1-config`

Transform a config file of a v1 Klio job (see [migration hub](../../../v2-migration)) to be compatible with a v2 Klio job. This command overwrites the existing config file.

```sh
Usage: klio job convert-v1-config [OPTIONS]

  Transforms a v1 config file to be compatible with klio v2 and overwrites
  the existing config file.

Options:
  -j, --job-dir PATH      Job directory where the job's ``Dockerfile`` is
                          located. Defaults current working directory.

  -c, --config-file PATH  Path to config filename. If ``PATH`` is not
                          absolute, it will be treated relative to ``--job-
                          dir``. Defaults to ``klio-job.yaml``.

  --help                  Show this message and exit.
```
### `klio job profile generate-entities`

The `klio job profile generate-entities` command generates a list of entity ids that can be used to profile the job at scale.

```sh
$ klio job profile generate-entities

Running query ...
spotify:track:4EVqL5qgaz5A821eVqYci7
spotify:track:0k5U7ZMdTVPDq9pqEjEvYc
spotify:track:3EhhT8jjmykJSOSATHrXwU
spotify:track:2iw4lto6vqmdI6i1TYvCYw
spotify:track:04TdocGiAGJhPXtXGeyi2Z
spotify:track:2rml5yuHVhvPGHDVouAsfW
spotify:track:5tYDFSHhXEFzONVGoOMDLK
spotify:track:4wYw7HUdIR4OTuNsE1cdX4
spotify:track:106S9830d8rACzt9QgV9jV
spotify:track:4TfQSTrnP89quqFIjnNZX4
```

Available options:

```sh
$ klio job profile generate-entities --help
Usage: klio job profile generate-entities [OPTIONS]

  Generate a list of entity ids to profile a job with

Options:
  -c, --config-file PATH          Path to config filename. If PATH is not
                                  absolute, it will be treated relative to
                                  `--job-dir`. Defaults to `klio-job.yaml`.

  -o, --output-file FILE          Output file for results.
  --track-min-length INTEGER      Minimum track length, in seconds. Defaults
                                  to 30.

  --track-max-length INTEGER      Minimum track length, in seconds. Defaults
                                  to 600.

  --number-of-tracks INTEGER      Number of tracks. Defaults to 10.
  --requested-format [file_id|audio_uri|audio_id|track_uri|track_id|track_gid]
  --help                          Show this message and exit.
```

Using the `--config-file` flag will use a query in your config file (defaulting to `klio-job.yaml`) to generate a list of entity ids that can be used to profile the job at scale.  To use this, add a `query_for_test_data` key under `job_config`, and put your BigQuery code there:

```yaml
# <-- snip -->
job_config:
  query_for_test_data: |
    SELECT * FROM project_foo.dataset_bar.table_baz
```
