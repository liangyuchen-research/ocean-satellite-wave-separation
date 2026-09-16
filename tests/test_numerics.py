"""Small numerical regressions independent of satellite data and TensorFlow."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from swath_rossby_wave import build_h_matrix2, build_hswath_matrix2, inversion, skill_matrix


class NumericalChecks(unittest.TestCase):
    def setUp(self):
        self.field = np.array([[[1.0, np.nan], [2.0, 3.0]]])
        self.lon = np.array([-124.0, -123.0])
        self.lat = np.array([32.0])
        self.time = np.array([0.0, 86400.0])
        self.k = np.array([[0.4, 0.6]])
        self.l = np.array([[0.1, 0.2]])
        self.psi = np.array([[1.0, 0.8]])
        self.radius = np.array([0.5, 0.6])

    def test_finite_observations_align_with_two_mode_basis(self):
        matrix, observations = build_h_matrix2(
            self.field, 2, self.k, self.l, self.lon, self.lat,
            self.time, self.psi, self.radius, 0,
        )
        self.assertEqual(matrix.shape, (3, 4))
        np.testing.assert_array_equal(observations, [1.0, 2.0, 3.0])
        self.assertTrue(np.isfinite(matrix).all())

    def test_skill_ignores_masked_and_nan_values(self):
        result, observations, i, j, t = skill_matrix(
            self.field, self.psi, self.k, self.l, 2,
            self.radius, self.lon, self.lat, self.time,
        )
        self.assertEqual(result.shape, (1, 1, 2))
        np.testing.assert_array_equal(observations, [1.0, 2.0, 3.0])
        self.assertEqual(len(i), len(observations))
        self.assertTrue(np.isfinite(result).all())

    def test_swath_supports_multiple_modes(self):
        lon_swath = self.lon[None, :]
        lat_swath = np.full((1, 2), self.lat[0])
        matrix = build_hswath_matrix2(
            self.field, 2, self.k, self.l, self.lon, self.lat,
            lon_swath, lat_swath, np.where(np.ones((1, 2))),
            self.time, self.psi, self.radius, 0,
        )
        self.assertEqual(matrix.shape, (4, 4))
        self.assertTrue(np.isfinite(matrix).all())

    def test_regularized_solve_and_bad_inputs(self):
        coefficients, estimate = inversion(np.array([2.0, 4.0]), np.eye(2), np.eye(2))
        np.testing.assert_allclose(coefficients, [1.0, 2.0])
        np.testing.assert_allclose(estimate, [1.0, 2.0])
        with self.assertRaises(ValueError):
            inversion(np.array([np.nan, 4.0]), np.eye(2), np.eye(2))
        with self.assertRaises(ValueError):
            inversion(np.array([2.0]), np.eye(2), np.eye(2))


if __name__ == '__main__':
    unittest.main()
