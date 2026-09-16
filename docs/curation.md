# Source and maintenance notes

All 56 original files from the two research collections were copied unchanged
into a separate local archive. Checkpoints, NetCDF data, notebook outputs and
source files were verified against SHA-256 manifests (approximately 444 MB).
Before this maintenance pass, all 19 published notebooks were also preserved
with a separate hash manifest. No original research data was modified.

## Maintained model collection

Eight model notebooks retain their source architectures, numeric hyperparameters
and validation protocol. Maintenance changes include English names, cleared
outputs, repository-relative paths, training opt-in and output overwrite guards.
Explicit float32 channel axes now align inputs and targets across current Keras
backends. Model export uses `.keras`; the dense-decoder notebook now exports and
predicts with its actual `model` variable rather than an undefined `autoencoder`.
Its dense output size is converted to a Python integer. The primary inference
NetCDF export preserves the named `sets`, `days`, `points` dimension order.
Input NetCDF handles are closed after reading arrays, allowing clean file
release on Windows as well as Unix systems.

All eight maintained model notebooks were executed cell by cell using small
synthetic inputs, one training epoch and batch size one. Model export, reload
and prediction equality passed with TensorFlow 2.20.0 and Keras 3.15.1.
`constraints-tested.txt` records the tested Python 3.12 dependency versions.
These bounded runs verify program execution, not historical model performance.

Rossby helpers now exclude masked/NaN observations without trailing zero rows,
allocate basis columns for every requested vertical mode, and solve regularized
systems without explicit matrix inversion. Physical units and regularization
choices were not reinterpreted.

## Historical material

Eight raw preprocessing notebooks and the alternative spatial projection remain
preserved locally because their full upstream prerequisites are unavailable.
Two model drafts are also preserved locally: the expanded spatial draft mixes
Conv2D with a spatial/time rank it does not support, and the adversarial draft
has unresolved discriminator update/loss behavior. They are not listed as
runnable examples. No substitute algorithm was invented to replace them.

[notebook-provenance.json](notebook-provenance.json) identifies maintained and
archived notebooks, original names and source hashes. Near-duplicate notebooks
and unrelated MNIST practice remain in the original preservation archive.

The numerical helper's authorship is not inferred from its presence in a local
folder. See [NOTICE.md](../NOTICE.md) for attribution and reuse boundaries.
