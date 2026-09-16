# Reproduction guide

## Maintained model workflow

Start Jupyter from the repository root or a notebook subdirectory. The bootstrap
finds `src/project_paths.py`, without using a machine-specific location.
`OCEAN_DATA_DIR` overrides `data/`. `OCEAN_ARTIFACT_DIR` overrides `artifacts/`;
model outputs use a separate subdirectory per notebook.

1. Install `requirements-models.txt` in a separate Python 3.12 environment.
2. Restore `new2_ssh_training_data.nc` and `new2_ssh_testing_data.nc` using
   `scripts/restore_artifacts.py --source /path/to/archive --only canonical`.
3. Open `notebooks/modeling/05_train_swath_autoencoder.ipynb`.
4. Review shapes, validation use and the original 30,000-epoch setting.
5. Set `ALLOW_TRAINING = True` and run the remaining cells.

Restoration verifies SHA-256 hashes and never overwrites a different file.
Newly trained models use `.keras`. Archived `.h5` checkpoints record Keras 2.6.0
and are separate from the maintained model-loading route.

For a standalone check with no research data, run
`python scripts/check_model_notebooks.py --notebook 05_train_swath_autoencoder`.
The checker creates small synthetic NetCDF inputs in a temporary directory,
executes every code cell with one epoch and batch size one, and compares saved
model inference with the in-memory model. Configuration overrides exist only
in that test run; no notebook or research input is edited.

## Experiment inputs

| Notebook | Input pair |
| --- | --- |
| `05_train_swath_autoencoder` | `new2_ssh_*_data.nc` |
| `small_dataset_flattened_autoencoder` | `ssh_*_data.nc` |
| `small_dataset_spatial_autoencoder` | `ssh_*_data2D.nc` |
| `expanded_flattened_autoencoder` | `new_ssh_*_data.nc` |
| `extended_spatial_autoencoder` | `new2_ssh_*_data2D.nc` |
| `convolutional_dense_decoder` | `new_ssh_*_data.nc` |
| `tanh_autoencoder` and `tanh_autoencoder_variant` | `new_ssh_*_data.nc` |

The star denotes separate `training` and `testing` filenames. Each input is
listed in `data/artifact-manifest.json`. Tanh experiments add random noise to
the target rather than using the supplied mixed signal, so their noise
configuration differs from the canonical notebook.

## Historical upstream preprocessing

The original preparation fits Rossby-wave coefficients to AVISO anomalies,
constructs a SWOT projection matrix, synthesizes internal waves, and combines
the fields into derived model inputs. Its notebooks remain in the local research
archive, with source hashes in [notebook-provenance.json](notebook-provenance.json).
They are outside the maintained executable collection.

Fresh raw-data reproduction requires four unavailable dependencies:

- `internal_waves.py`, including `SpectralDomain`, Garrett-Munk spectral helpers,
  `make_synthetic_field`, and `abel_integral`.
- `aviso_tot_MSLA_ccs.mat`, with `dsave`, `tsave`, `xsave`, and `ysave`.
- `aviso_tot_MSLA_ccs_data.nc`, used for swath construction and projection.
- `stratification_sample_ccs.nc`, including vertical-mode structure `Psi`.

These must come from the original scientific source. The available
`aviso_msla_ccs_1d.nc` has different dimensions and cannot replace the MATLAB
input. No replacement physics implementation has been inferred from filenames
or downstream calls.
