# `spotify-klio`

The `spotify-klio` provides additional utilities to the [`klio`](https://klio.readthedocs.io/en/latest/reference/lib/index.html) library to work with Spotify's infrastructure.

## `KlioReadFromHadesAvro`

Located in `spotify_klio.transforms.io`, the `KlioReadFromHadesAvro` transform that can be used to read [event input](https://klio.readthedocs.io/en/latest/userguide/io/index.html) for a Klio **batch** pipeline.

The `KlioReadFromHadesAvro` is **automatically used** when a batch Klio job is configured as such:

```yaml
# <-- snip -->
pipeline_options:
  streaming: False
  # <-- snip -->
job_config:
  events:
    input:
      - type: avro
        location: hades:///my-input-endpoint
```

## `HadesClient`

Located in `spotify_klio.transforms.clients`, the `HadesClient` class can be used for making requests to [Hades](https://backstage.spotify.net/docs/hades/). 

This client is used automatically when using the [`KlioReadFromHadesAvro`](#klioreadfromhadesavro) transform.
