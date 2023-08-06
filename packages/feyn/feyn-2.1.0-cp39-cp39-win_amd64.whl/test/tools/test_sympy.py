import unittest
from typing import List

from feyn.tools import sympify_model
from feyn import Model

from feyn.tools._sympy import _signif

import numpy as np
import sympy

from .. import quickmodels


class TestTools(unittest.TestCase):
    def setUp(self) -> None:
        self.data = dict(
            {
                "age": np.array([20, 40, 20, 20, 40, 20]),
                "smoker": np.array([0, 1, 1, 0, 1, 0]),
                "sex": np.array(["yes", "no", "yes", "no", "yes", "no"]),
                "charges": np.array([10000, 20101, 10001, 20101, 20100, 10101]),
            }
        )

    def test_signif(self):
        digits = 6

        with self.subTest("Can round floats to significant digits (rather than decimal points)"):
            num = 12345.12345

            expected = 12345.1
            actual = _signif(num, digits)

            self.assertEqual(expected, actual, "Expected signif to round properly")

        with self.subTest("Can round scientific notation as well as floats"):
            from sympy import sympify

            num = sympify(f"{12345.12345:10e}")

            expected = round(sympy.Float(12345.1), 1)
            actual = _signif(num, digits)

            assert isinstance(actual, sympy.Float)
            self.assertEqual(expected, actual, "Expected signif to round properly")

        with self.subTest("Can round integers to significant digits"):
            num = 1234

            expected = 1230
            actual = _signif(num, 3)
            self.assertEqual(expected, actual, "Expected signif to round properly")

    def test_predict_sympy_all(self):
        model = quickmodels.get_simple_binary_model(["age", "smoker"], "charges")

        expected = model.predict(self.data)

        signif = 15

        symp = sympify_model(model, symbolic_lr=True, signif=signif)

        actual = _predict_sympy_all(symp, self.data, model, signif)
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a, places=signif - 5)  # These places are after decimal

    def test_weightless_sympy(self):
        model = quickmodels.get_simple_binary_model(["age", "smoker"], "charges")

        symp = sympify_model(model, symbolic_lr=True, include_weights=False)

        assert "age + smoker" == str(symp)

    def test_sympy_underscores_get_replaced(self):
        model = quickmodels.get_simple_binary_model(["age_age", "sex"], "charges")
        self.data["age_age"] = self.data["age"]
        del self.data["age"]

        symp = sympify_model(model, symbolic_lr=True, include_weights=False)

        assert "ageage + sex" == str(symp)

    def test_sympy_symboliclr_false(self):
        model = quickmodels.get_simple_binary_model(["age", "sex"], "charges", stypes={"charges": "b"})

        symp = sympify_model(model, symbolic_lr=False, include_weights=False)

        assert "logreg(age + sex)" == str(symp)

    def test_sympy_symboliclr_true(self):
        model = quickmodels.get_simple_binary_model(["age", "sex"], "charges", stypes={"charges": "b"})

        symp = sympify_model(model, symbolic_lr=True, include_weights=False)

        assert "1/(exp(-age - sex) + 1)" == str(symp)


def _predict_sympy_all(expr, samples, model, signif=15):
    mappings = get_mappings(model)
    predictions = []

    length = len(next(iter(samples.values())))
    for i in range(length):
        sample = {key: values[i : i + 1] for key, values in samples.items()}
        prediction = expr.evalf(n=signif, subs=_prepare_args(sample, mappings))
        predictions.append(prediction)

    return predictions


def _prepare_args(sample, mappings):
    result = {}
    for col in sample.keys():
        name = col.replace(" ", "")  # spaces turn to nothing
        if name in mappings:
            category_value = sample[name][0]
            result[name + "_cat"] = mappings[name][category_value]
            continue

        result[name] = sample[name][0]
    return result


def get_mappings(model):
    mapped_categories = dict()
    for elm in model:
        if elm.fname == "cat":
            mapped_categories[elm.name] = elm.params["categories"]
    return mapped_categories
