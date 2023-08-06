import unittest
import pandas as pd

from feyn.tools._model_params_dataframe import (
    get_model_parameters,
    _determine_categories,
    _determine_initial_df_and_merge_args,
    _params_dataframe
)

from .. import quickmodels


class TestFeatParamDF(unittest.TestCase):

    def setUp(self) -> None:
        self.simple_model = quickmodels.get_simple_binary_model(
            ['banana', 'x'],
            'y',
            stypes={'banana': 'c'}
        )
        self.simple_model[0].params.update({
            'scale': 0.5,
            'w': -1.22,
            'bias': 0.023
        })
        self.simple_model[2].params.update({
            'categories': [('u', -0.026), ('m', 0.016), ('y', 0.026)],
            'bias': 0.51
        })
        self.simple_model[3].params.update({
            'scale': 0.5,
            'w': -0.55,
            'bias': 0.046
        })

    def test_raises_value_error_when_feature_not_in_model(self):
        with self.assertRaises(ValueError) as ctx:
            feature_name = 'kittens'
            get_model_parameters(
                self.simple_model, feature_name=feature_name
            )
        self.assertEqual(
            f"{feature_name} not in model inputs or output!", str(ctx.exception)
        )

    def test_determine_categories(self):
        expected = ['banana']
        actual = _determine_categories(self.simple_model)

        self.assertListEqual(expected, actual)

    def test_determine_initial_df_and_merge_args(self):
        with self.subTest(
            "If feature is categorical"
        ):
            feature_name = 'banana'
            expected_df = pd.DataFrame(columns=['banana'])
            expected_args = {'on': 'banana'}

            actual_df, actual_args = _determine_initial_df_and_merge_args(feature_name, True)
            pd.testing.assert_frame_equal(expected_df, actual_df)
            self.assertDictEqual(expected_args, actual_args)

        with self.subTest(
            "If feature is numerical"
        ):
            feature_name = 'x'
            expected_df = pd.DataFrame()
            expected_args = {'left_index': True, 'right_index': True}

            actual_df, actual_args = _determine_initial_df_and_merge_args(feature_name, False)
            pd.testing.assert_frame_equal(expected_df, actual_df)
            self.assertDictEqual(expected_args, actual_args)

    def test_params_dataframe(self):
        model = self.simple_model
        with self.subTest(
            "If elem is a categorical input, columns should be the feature name and 'weights'"
        ):
            expected = ['banana', 'weights']
            actual = _params_dataframe(model[2]).columns
            self.assertListEqual(expected, list(actual))

        with self.subTest(
            "If elem is a numerical input, columns should be the feature name"
        ):
            expected = ['x']
            actual = _params_dataframe(model[3]).columns
            self.assertListEqual(expected, list(actual))

        with self.subTest(
            "If elem is a numerical output, columns should be the models output"
        ):
            expected = [model.output]
            actual = _params_dataframe(model[0]).columns
            self.assertListEqual(expected, list(actual))

        with self.subTest(
            "If elem is any other function"
        ):
            expected = pd.DataFrame()
            actual = _params_dataframe(model[1])
            pd.testing.assert_frame_equal(expected, actual)

    def test_get_model_parameters_simple_model(self):
        model = self.simple_model
        with self.subTest(
            "If feature is categorical"
        ):
            expected = pd.DataFrame(
                [('y', 0.026), ('m', 0.016), ('u', -0.026)],
                columns=['banana', 'weights']
            )
            actual = get_model_parameters(model, 'banana')
            pd.testing.assert_frame_equal(expected, actual)

        with self.subTest(
            "If feature is numerical"
        ):
            expected = pd.DataFrame(
                data=[0.5, -0.55, 0.046],
                columns=['x'],
                index=['scale', 'w', 'bias']
            )
            actual = get_model_parameters(model, 'x')
            pd.testing.assert_frame_equal(expected, actual)

        with self.subTest(
            "If feature is the output"
        ):
            expected = pd.DataFrame(
                data=[0.5, -1.22, 0.023],
                columns=[model.output],
                index=['scale', 'w', 'bias']
            )
            actual = get_model_parameters(model, 'y')
            pd.testing.assert_frame_equal(expected, actual)

    def test_get_model_parameters_complex_model(self):
        complex_model = quickmodels.get_quaternary_model(
            ['banana', 'x', 'banana', 'x'], 'y', stypes={'banana': 'c'}
        )
        for idx, elem in enumerate(complex_model):
            if elem.fname == "in:cat":
                complex_model[idx].params.update({
                        'categories': [('y', 0.1), ('u', 0.2), ('m', 0.3)],
                        'bias': 0.01
                })
            elif elem.fname == "in:linear" or 'out:' in elem.fname:
                complex_model[idx].params.update({
                    'scale': 0.5,
                    'w': 1.,
                    'bias': 0.05
                })

        with self.subTest(
            "If categorical feature has multiple inputs, the columns should be the feature name and \
            weights_[elem_index], where elem_index corresponds to the index of each input"
        ):
            expected = ['banana', 'weights_4', 'weights_6']
            actual = get_model_parameters(complex_model, 'banana').columns
            self.assertListEqual(expected, list(actual))

        with self.subTest(
            "If numerical feature has multiple inputs, the columns should be feature_[elem_index], \
                where elem_index corresponds to the index of each input"
        ):
            expected = ['x_5', 'x_7']
            actual = get_model_parameters(complex_model, 'x').columns
            self.assertListEqual(expected, list(actual))
