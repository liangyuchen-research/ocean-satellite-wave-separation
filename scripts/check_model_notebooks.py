"""Execute a bounded model notebook with synthetic NetCDF inputs.

This checks code execution, tensor shapes, one training epoch, exports and model
reload. It does not reproduce a scientific experiment or assess model quality.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
from pathlib import Path
import re
import tempfile

os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('TF_NUM_INTEROP_THREADS', '2')
os.environ.setdefault('TF_NUM_INTRAOP_THREADS', '2')


def main():
    root = Path(__file__).resolve().parents[1]
    notebooks = {p.stem: p for p in root.glob('notebooks/**/*.ipynb')}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notebook', choices=sorted(notebooks), required=True)
    args = parser.parse_args()

    import numpy as np
    import tensorflow as tf
    import xarray as xr

    notebook = json.loads(notebooks[args.notebook].read_text(encoding='utf8'))
    sources = [''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code']
    data_names = re.findall(r"file_path = r?['\"]([^'\"]+\.nc)['\"]", '\n'.join(sources))
    with tempfile.TemporaryDirectory(prefix='ocean-model-check-') as temporary:
        work = Path(temporary)
        rng = np.random.default_rng(42)
        for name in data_names:
            split = 'training' if 'training' in name else 'testing'
            dims = ('x', 'y', 'days', 'sets') if '2D' in name else ('points', 'days', 'sets')
            shape = (3, 3, 4, 12) if '2D' in name else (6, 4, 12)
            target = rng.normal(0, 0.01, shape).astype('float32')
            noisy = target + rng.normal(0, 0.002, shape).astype('float32')
            xr.Dataset({
                f'ssh_{split}_data': (dims, noisy),
                f'ssh_{split}_target': (dims, target),
            }).to_netcdf(work / name)
        os.environ['OCEAN_DATA_DIR'] = str(work)
        os.environ['OCEAN_ARTIFACT_DIR'] = str(work / 'artifacts')
        namespace = {'__name__': '__model_check__'}
        with contextlib.chdir(root):
            for index, source in enumerate(sources):
                # Bound computation without editing the scientific notebook.
                source = re.sub(r'\bEpoch\s*=\s*\d+', 'Epoch = 1', source)
                source = re.sub(r'\bbatch_size\s*=\s*\d+', 'batch_size=1', source)
                exec(compile(source, f'{args.notebook}:code-{index}', 'exec'), namespace)
                if 'ALLOW_TRAINING' in namespace:
                    namespace['ALLOW_TRAINING'] = True
        saved = list((work / 'artifacts').rglob('*.keras'))
        if len(saved) != 1:
            raise AssertionError('Expected one exported Keras model.')
        restored = tf.keras.models.load_model(saved[0], compile=False)
        sample = namespace['testing'][:1]
        original = namespace.get('autoencoder', namespace.get('model'))
        expected = original(sample, training=False).numpy()
        actual = restored(sample, training=False).numpy()
        np.testing.assert_allclose(actual, expected, rtol=1e-5, atol=1e-6)
        if actual.shape != sample.shape or not np.isfinite(actual).all():
            raise AssertionError('Reconstruction shape or numerical output is invalid.')
        print(f'PASS {args.notebook}: every code cell, one synthetic epoch, export, reload and inference')
        print(f'TensorFlow {tf.__version__}; Keras {tf.keras.__version__}; NumPy {np.__version__}')


if __name__ == '__main__':
    main()
