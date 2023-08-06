# `spotify-klio-exec`

Internal plugins for the [`klio-exec`](https://klio.readthedocs.io/en/latest/reference/executor/index.html) tool.

The `klio-exec`  (which `spotify-klio-exec` supplements) provides a CLI that is **not** meant to be used directly ([more about the ecosystem](https://klio.readthedocs.io/en/latest/reference/index.html#ecosystem)).

## Supplementary Functionality

### Default XPN (Cross-Project Networking) Support

In order to connect to internal services (backend services, artifactory, etc), a Dataflow job will need to be within the XPN network. While, the [desired subnetwork](https://backstage.spotify.net/docs/data-engineering-golden-path/part-7-streaming-pipelines/8-faq/#subnetwork) may be added to `pipeline_options.subnetwork`, `spotify-klio-exec` will automatically set this up for a job. 

If you do not neet XPN networking, then [run your job](https://backstage.spotify.net/docs/klio/cli/klio/usage/#klio-job-run) with the flag `--no-xpn`, e.g. `klio job run --no-xpn`.

### Read Avro from Hades

`spotify-klio-exec` adds support for reading avro from Hades for a batch job [when configured](https://backstage.spotify.net/docs/klio/lib/klio/usage/#klioreadfromhadesavro).
