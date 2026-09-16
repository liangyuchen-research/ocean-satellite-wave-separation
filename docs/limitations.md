# Scientific and implementation limitations

## Evaluation

The notebook sources repeatedly pass arrays named `testing` as Keras validation
data during training. Training curves or final values from those arrays do not
constitute an independent final test. The 1% or 10% random split created within
some notebooks is not consistently used by their training call.

Windows in the preprocessing notebooks overlap, and training/testing synthetic
internal-wave generators use the same seed value. Temporal independence and
the relationship between generated realizations require a separate audit before
claiming out-of-sample performance. No model-ranking or accuracy claim is made
from the historical output logs.

## Scientific scope

- The Rossby component is fit from AVISO SSH anomalies and projected onto sample
  SWOT track coordinates; synthetic internal-wave fields supply contamination.
- Source projection arrays assume particular track counts, sampling indices,
  dimensions and dates. They are research configurations, not arbitrary-domain APIs.
- Rossby-mode routines state that only one vertical mode was tested.
- Unit conversions, regularization settings and explicit matrix inversions retain
  the original implementation and have not received a scientific validation audit.
- The original `skill_matrix` includes a `value != np.nan` condition, which does
  not by itself reject NaNs. Its behavior was preserved, not silently redefined.
- Several model variants omit hidden-layer activations or have output activations
  that constrain the range. Their architectures are preserved as experiments.

## Reproducibility

The missing `internal_waves` module and upstream fields prevent a complete fresh
preprocessing run. Some legacy notebooks depend on specific TensorFlow/Keras
behavior and implicitly handled channel dimensions. The archived HDF5 models
record Keras 2.6.0, but there is no exact full environment lockfile.

The primary inference export's dimension names were corrected to match its
transposed array order (`sets`, `days`, `points`) and its output filename was
changed so it cannot replace the input dataset. These are documented curation
changes, not evidence of newly validated model performance.

Only lightweight syntax, schema, path-protection and small numerical checks were
run. No training, expensive projection or full satellite-data analysis was executed.
