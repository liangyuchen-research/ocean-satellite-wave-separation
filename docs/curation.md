# Source and maintenance notes

All 56 original files from the two source collections, including checkpoints,
NetCDF data, HDF5 models and notebook outputs, were copied unchanged into a local
preservation archive. Every copy was verified against a SHA-256 manifest. The
archive is separate from this repository and contains about 444 MB.

## Repository changes

- Renamed notebooks to English descriptions and grouped preprocessing, modeling
  and alternative experiments.
- Cleared notebook outputs, execution counts and transient metadata.
- Preserved English comments and scientific computation logic.
- Replaced machine-specific paths with repository-relative input/output helpers.
- Added an explicit training opt-in before long-running training calls.
- Protected existing generated outputs from silent replacement.
- Corrected MAE curve labels that were originally marked as MSE.
- Added the missing training internal-wave export using the testing export schema.
- Redirected the primary inference export to `swath_inference_results.nc` and
  corrected its dimension names to `sets`, `days`, `points`.
- Kept the training-projection notebook's final exploratory cells 15-18 only in
  the unchanged archive. Those cells read an unavailable scratch file and then
  overwrite the training dataset with mislabeled variables; they are not part
  of the canonical preprocessing sequence.

`notebook-provenance.json` maps each notebook to its original name and
source hash. Near-duplicate `UCSD-1D-Copy1`, `UCSD-Copy1`, and `new2 UCSD-1D`
notebooks remain in the local archive. The unrelated MNIST practice notebook
`Untitled.ipynb` also remains archived rather than being presented as ocean research.

The preserved `swath_rossby_wave.py` has only whitespace and punctuation cleanup.
Authorship is not inferred from its presence in a local folder.
