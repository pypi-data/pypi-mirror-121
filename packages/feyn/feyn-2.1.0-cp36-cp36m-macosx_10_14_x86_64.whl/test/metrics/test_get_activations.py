import unittest

import numpy as np

from feyn.metrics._metrics import _get_activations
from .. import quickmodels

class TestModelActivations(unittest.TestCase):

    def test_computes_activations(self):
        model = quickmodels.get_identity_model()

        x = np.array([1,2,3,4])
        activations = _get_activations(model, {"x": x})
        np.testing.assert_array_equal(activations[1], x*.5-.5)
        np.testing.assert_array_equal(activations[0], x)

