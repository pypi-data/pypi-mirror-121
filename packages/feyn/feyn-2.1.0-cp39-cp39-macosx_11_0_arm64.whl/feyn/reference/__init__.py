"""
This module contains reference models that can be used for comparison with feyn models.
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from pandas import DataFrame
import typing

from .._base_reporting_mixin import BaseReportingMixin

class BaseReferenceModel(BaseReportingMixin, metaclass=ABCMeta):
    @abstractmethod
    def predict(self, X: typing.Iterable):
        raise NotImplementedError()


class ConstantModel(BaseReferenceModel):
    def __init__(self, target: str, const: float):
        """Create a Constant Model on your dataset.

        This will always return the same value, regardless of the samples you provide it.

        Arguments:
            target {str} -- The output column of your dataset.
            const {float} -- The constant to return (for instance, you can choose the mean of your dataset).
        """
        self.const = const
        self.target = target

    def predict(self, data: typing.Iterable):
        return np.full(len(data), self.const)


class SKLearnClassifier(BaseReferenceModel):
    def __init__(self, sklearn_classifier:type, data: DataFrame, target: str, **kwargs):
        """Creates a base SKLearn Classifier on your dataset.

        Arguments:
            sklearn_classifier {type} -- The sklearn model type you want to wrap. (example: sklearn.linear_model.LogisticRegression).
            data {DataFrame} -- The data to fit on.
            target {str} -- The output column of your dataset.
        """
        self.features = list(data.columns)
        if target in self.features:
            self.features.remove(target)

        self.target = target

        self._model = sklearn_classifier(**kwargs)
        self._model.fit(X=data[self.features], y=data[self.target])

    def predict(self, X: typing.Iterable):
        if type(X).__name__ == "DataFrame":
            X = X[self.features].values

        elif type(X).__name__ == "dict":
            X = np.array([X[col] for col in self.features]).T

        pred = self._model.predict_proba(X)[:, 1]
        return pred


class LogisticRegressionClassifier(SKLearnClassifier):
    def __init__(self, data: DataFrame, target: str, **kwargs):
        """Create a Logistic Regression Classifier on your dataset.

        This calls sklearn.linear_model.LogisticRegression under the hood.
        It has no special handling for categoricals, so you need to keep that in mind while using it.

        Arguments:
            data {DataFrame} -- The data to fit on.
            target {str} -- The output column of your dataset.
        """
        import sklearn.linear_model
        if "penalty" not in kwargs:
            kwargs["penalty"]="none"
        super().__init__(sklearn.linear_model.LogisticRegression, data, target, **kwargs)

    def summary(self, ax=None):
        import pandas as pd
        return pd.DataFrame(data={"coeff": self._model.coef_[0]}, index=self.features)


class RandomForestClassifier(SKLearnClassifier):
    def __init__(self, data: DataFrame, target: str, **kwargs):
        """Create a Random Forest Classifier on your dataset.

        This calls sklearn.ensemble.RandomForestClassifier under the hood.
        It has no special handling for categoricals, so you need to keep that in mind while using it.

        Arguments:
            data {DataFrame} -- The data to fit on.
            target {str} -- The output column of your dataset.
        """
        import sklearn.ensemble
        super().__init__(sklearn.ensemble.RandomForestClassifier, data, target, **kwargs)


class GradientBoostingClassifier(SKLearnClassifier):
    def __init__(self, data: DataFrame, target: str, **kwargs):
        """Create a Gradient Boosting Classifier on your dataset.

        This calls sklearn.ensemble.GradientBoostingClassifier under the hood.
        It has no special handling for categoricals, so you need to keep that in mind while using it.

        Arguments:
            data {DataFrame} -- The data to fit on.
            target {str} -- The output column of your dataset.
        """
        import sklearn.ensemble
        super().__init__(sklearn.ensemble.GradientBoostingClassifier, data, target, **kwargs)



class SKLearnRegressor(BaseReferenceModel):
    def __init__(self, sklearn_regressor:type, data: DataFrame, target: str, **kwargs):
        """Creates a base SKLearn regressor on your dataset.

        Arguments:
            sklearn_regressor {type} -- The sklearn model type you want to wrap. (example: sklearn.linear_model.LinearRegression).
            data {DataFrame} -- The data to fit on.
            target {str} -- The output column of your dataset.
        """
        self.features = list(data.columns)
        if target in self.features:
            self.features.remove(target)

        self.target = target

        self._model = sklearn_regressor(**kwargs)
        self._model.fit(X=data[self.features], y=data[self.target])

    def predict(self, X: typing.Iterable):
        if type(X).__name__ == "DataFrame":
            X = X[self.features].values

        elif type(X).__name__ == "dict":
            X = np.array([X[col] for col in self.features]).T

        pred = self._model.predict(X)
        return pred


class LinearRegression(SKLearnRegressor):
    def __init__(self, data: DataFrame, target: str, **kwargs):
        """Create a Linear Regression model on your dataset.

        This calls sklearn.linear_model.LinearRegression under the hood.
        It has no special handling for categoricals, so you need to keep that in mind while using it.

        Arguments:
            data {DataFrame} -- The data to fit on.
            target {str} -- The output column of your dataset.
        """
        import sklearn.linear_model

        super().__init__(sklearn.linear_model.LinearRegression, data, target, **kwargs)
