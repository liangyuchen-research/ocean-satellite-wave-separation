# Scientific and implementation limitations

## Evaluation

The sources pass arrays named `testing` as Keras validation data during training.
Those curves are not an independent final test. The 1% or 10% random split
within notebooks is not consistently used by their training call.

Preprocessing windows overlap, and training/testing internal-wave generators use
the same seed. A separate temporal or geographic holdout is needed to assess
generalization. No accuracy or model-ranking claim is made from historical logs.

## Scientific scope

- The Rossby component is fit from AVISO anomalies and projected onto sampled
  SWOT coordinates. Synthetic internal-wave fields supply contamination.
- Projection arrays assume specific track counts, dates, dimensions and units.
- Unit conversions and regularization values remain those of the source.
- Missing/invalid observations are now excluded consistently, matrix columns
  include all requested vertical modes, and regularized inversion uses a linear
  solve rather than explicitly forming an inverse. Small tests cover these
  corrections; they are not a physical validation of the Rossby model.
- Several variants omit hidden activations or constrain output range. Their
  architectures remain research experiments, not recommended production models.

## Runtime and source availability

Maintained notebooks use explicit float32 channel axes and the `.keras` export
format. The original Keras 2.6 HDF5 checkpoints have not been promoted to verified
model releases. Full historical training has not been repeated.

The upstream `internal_waves` module and three input fields were not located.
Raw preprocessing is therefore preserved in the local archive, outside the
maintained model route. An expanded spatial notebook with incompatible Conv2D
inputs, and an adversarial notebook with unresolved discriminator training logic,
are also archived rather than presented as working model examples. All original
files and the previous public notebook versions remain preserved.
