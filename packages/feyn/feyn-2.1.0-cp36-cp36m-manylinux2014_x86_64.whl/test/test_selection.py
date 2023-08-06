from typing import Tuple, List
import pytest

import feyn
import unittest

from . import quickmodels
from feyn._selection import _remove_duplicates

class TestPruning(unittest.TestCase):
    def setUp(self):
        self.test_model = quickmodels.get_unary_model(["bmi"], "sex")
        self.test_models = [self.test_model] * 3

    def test_duplicates_are_pruned(self):
        hashset = set(hash(m) for m in self.test_models)
        pruned = feyn.prune_models(self.test_models)
        self.assertEqual(len(pruned), len(hashset))

    def test_keeping_no_more_than_n_models(self):
        unique_models = quickmodels.get_n_unique_models(20)
        pruned_models = feyn.prune_models(unique_models, keep_n=5)
        self.assertEqual(5, len(pruned_models))

class TestRemoveDuplicates(unittest.TestCase):
    def setUp(self):
        self.test_model = quickmodels.get_simple_binary_model(["x", "y"], output="z")
        self.next_model = quickmodels.get_simple_binary_model(["x", "z"], output="y")

    def test_remove_duplicates(self):

        with self.subTest("Check duplicate model gets removed"):
            models = [self.test_model] * 2
            actual = _remove_duplicates(models)
            expected = [quickmodels.get_simple_binary_model(["x", "y"], output="z")]
            self.assertEqual(len(actual), len(expected))

        with self.subTest("Check different models don't get removed"):
            models = [self.test_model, self.next_model]
            actual = _remove_duplicates(models)
            expected = models
            self.assertEqual(len(actual), len(expected))

        with self.subTest("Check features with problematic characters"):
            # Check that no errors are raised
            model = quickmodels.get_simple_binary_model(["feature-with-dash", "feature.with.dot.character", "feature_with_underscore", "feature with space"], output="y")
            actual = _remove_duplicates([model, model])
