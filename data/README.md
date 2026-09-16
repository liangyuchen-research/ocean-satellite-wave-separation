# External data and checkpoints

This directory contains metadata only. NetCDF products, derived arrays and HDF5
models were preserved in the local source archive and excluded from Git commits.
`artifact-manifest.json` lists file names, sizes, SHA-256 hashes and restore targets.
It does not provide download authorization or a redistribution license.

## Available data groups

| Dataset prefix/layout | Training sets | Testing sets | Sample layout |
| --- | ---: | ---: | --- |
| `ssh_*_data.nc` | 13 | 6 | 277 points, 10 days |
| `new_ssh_*_data.nc` | 79 | 40 | 277 points, 10 days |
| `new2_ssh_*_data.nc` | 117 | 59 | 277 points, 20 days |
| Corresponding `data2D.nc` files | Same set counts | Same set counts | 8 by 34 spatial samples, time, sets |

Derived arrays are named `ssh_training_data`, `ssh_training_target`,
`ssh_testing_data` and `ssh_testing_target`. The target is the projected Rossby
component; input includes a synthetic internal-wave contribution.

Two SWOT Level 2 Low Rate Expert SSH granules carry identifiers 474/013 and
474/026 with 29 March 2023 timestamps. Their internal metadata identifies JPL,
Ka-band radar interferometer observations and reference V1.1. The approximately
247 MB AVISO file has no verified original download URL in the supplied material.
Product-level attribution and usage terms must be checked at the original source
before redistributing these products or derivatives.

The two HDF5 model files record TensorFlow backend and Keras 2.6.0. Their training
lineage has not been matched conclusively to one notebook run, so they are archived
artifacts rather than advertised verified releases.

To restore from an authorized copy of the local archive, run:

```bash
python scripts/restore_artifacts.py --source /path/to/source-archive
```

The restore script searches the source directory by hash, copies matching files
to `data/`, and refuses to overwrite a differing destination. It does not delete
source files or download data. Review storage needs before restoring all files.
Use `--only canonical` to restore only the two canonical model datasets.
