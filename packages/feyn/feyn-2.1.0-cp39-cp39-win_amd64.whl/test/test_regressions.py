"""
This file contains regression errors observed in production. Some of these tests may
be a bit gnarly formulated, they may be a bit more fragile, and they probably do not
smell like a requirement specification for the feyn.

The idea is, that these can be deleted whenever they become too annoying.
"""


import numpy as np

import feyn
import _feyn
from . import quickmodels

import unittest


class TestMiscRegressions(unittest.TestCase):
    def test_model_handles_nans(self):
        m = quickmodels.get_unary_model()

        with self.subTest("ValueError when Nan in input"):
            with self.assertRaises(ValueError) as ctx:
                data = {"x": [np.nan]}
                m.predict(data)

            self.assertIn("nan", str(ctx.exception))

        with self.subTest("ValueError when inf in input"):
            with self.assertRaises(ValueError) as ctx:
                data = {"x": [np.inf]}
                m.predict(data)

            self.assertIn("inf", str(ctx.exception))

        with self.subTest("ValueError when Nan in output"):
            with self.assertRaises(ValueError) as ctx:
                data = {"x": np.array([1.0]), "y": np.array([np.nan])}
                m._fit(data, loss_function=feyn.losses.squared_error)

            self.assertIn("nan", str(ctx.exception))

    def test_filter_works_with_numpy_int(self):
        features, output = list('abc'), 'output'

        models = [
            quickmodels.get_unary_model(features, output), # Complexity 2
            quickmodels.get_simple_binary_model(features, output) # Complexity 3
        ]

        n2 = sum(map(lambda m: m.edge_count == 2, models))
        complexity_filter = feyn.filters.Complexity(np.int64(2))

        filtered_models = list(filter(complexity_filter, models))
        self.assertEqual(n2, len(filtered_models))
