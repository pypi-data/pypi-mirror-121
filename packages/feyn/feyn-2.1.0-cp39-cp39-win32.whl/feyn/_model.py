"""Class for a feyn Model. A feyn Model is a composition of mathematical functions from some input features to an output."""

import json
from pathlib import Path
from typing import AnyStr, TextIO, Union, Optional, List
from pandas import DataFrame
import numpy as np

import _feyn
import feyn
from ._program import Program
from ._base_reporting_mixin import BaseReportingMixin
from ._plots_mixin import PlotsMixin
from ._interactivemixin import InteractiveMixin
from ._compatibility import supports_interactivity

# Update this number whenever there are breaking changes to save/load
# Then use it intelligently in Model.load.
SCHEMA_VERSION = "2021-08-30"

PathLike = Union[AnyStr, Path]


class Element:
    def __init__(self, model: "Model", ix: int) -> None:
        self._model = model
        self._ix = ix

    @property
    def opcode(self):
        if self._ix == 0:
            raise ValueError("No opcodes for model index=0 (output element)")

        return self._model._program[self._ix]

    @property
    def fname(self):
        return self._model.fnames[self._ix]

    @property
    def name(self):
        return self._model.names[self._ix]

    @property
    def params(self):
        return self._model.params[self._ix]

    @property
    def tooltip(self):
        # TODO: element tooltips - validate KEvin did a good job
        if self.fname == "in:linear" or self.fname=="out:linear":
            return f"{self.name}\nlinear:\nscale={self.params['scale']:6f}\nw={self.params['w']:.6f}\nbias={self.params['bias']:.4f}"
        elif self.fname == "linear":
            return f"linear:\nw={self.params['w0']:.6f}\nbias={self.params['bias']:.4f}"
        elif self.fname == "out:lr":
            return f"{self.name}\nlogistic:\nw={self.params['w']:.4f}\nbias={self.params['bias']:.4f}"
        elif self.fname == "in:cat":
            return (
                f"{self.name}\ncategorical with {len(self.params['categories'])} values\nbias={self.params['bias']:.4f}"
            )
        else:
            return self.fname

    @property
    def arity(self):
        return self._model._program.arity_at(self._ix)

    @property
    def children(self):
        if self.arity == 0:
            return []

        if self.arity == 1:
            return [self._ix + 1]

        if self.arity == 2:
            first_child_ix = self._ix + 1
            second_child_ix = self._model._program.find_end(first_child_ix)

            return [first_child_ix, second_child_ix]

        raise ValueError("Internal error")


class Model(
    BaseReportingMixin,
    PlotsMixin,
    InteractiveMixin if supports_interactivity() else object,
):
    """
    A Model represents a single mathematical equation which can be used for predicting.

    The constructor is for internal use.
    """

    def __init__(self, program, names, fnames, params=None):
        proglen = len(program)

        if proglen != len(names):
            raise ValueError("length of 'names' does not match program")

        if proglen != len(fnames):
            raise ValueError("length of 'fnames' does not match program")

        if not params:
            params = [{} for _ in names]

        if proglen != len(params):
            raise ValueError("length of 'params' does not match program")

        self.loss_values = []
        self.loss_value = None
        self.age = 0

        self._program = program
        self.names = names
        self.fnames = fnames
        self.params = params

        self._sample_count = 0

        self._elements = [Element(self, ix) for ix in range(len(self._program))]

        # Build a qepler
        self._qepler = self._build_qepler(program, names, fnames, params, self._sample_count)
        # Extract the newly created params from the qepler
        
        self.params = self._qepler.params

    def _build_qepler(self, program, dnames, fnames, params, sample_count):
        """
        Builds an internal qepler trainer to train this model.
        In a future refactor it will be instantiated when needed (in the sgdtrainer)
        """

        _qepler = _feyn.Model(dnames, fnames, sample_count)
        _qepler.params = params

        return _qepler


    @property
    def _paramcount(self):
        return sum([feyn.FNAME_MAP[fname]["paramcount"] for fname in self.fnames])


    def predict(self, X: DataFrame) -> np.ndarray:
        """
        Calculate predictions based on input values. Note that for classification tasks the output are probabilities.

        >>> model.predict({ "age": [34, 78], "sex": ["male", "female"] })
        [0.85, 0.21]

        Arguments:
            X {DataFrame} -- The input values as a pandas.DataFrame.

        Returns:
            np.ndarray -- The calculated predictions.
        """
        if type(X).__name__ == "dict":
            for k in X:
                if type(X[k]).__name__ == "list":
                    X[k] = np.array(X[k])

        # Magic support for pandas Series
        if type(X).__name__ == "Series":
            X = {idx: np.array([X[idx]]) for idx in X.index}

        # Magic support for pandas DataFrame
        if type(X).__name__ == "DataFrame":
            X = {col: X[col].values for col in X.columns}

        self._qepler.params = self.params

        res = self._qepler._query(X, None)
        self.params = self._qepler.params

        return res

    @property
    def edge_count(self) -> int:
        """Get the total number of edges in the graph representation of this model."""
        return len(self._program) - 1

    @property
    def depth(self) -> int:
        """Get the depth of the graph representation of the model. In general, it is better to evaluate the complexity of models using the edge_count (or max_complexity) properties"""
        return max(self._program.depths())

    def depths(self) -> List[int]:
        """Get the depth of each element in the model when presented as a graph"""
        return self._program.depths()

    @property
    def output(self) -> str:
        """Get the name of the output node. Does the same as 'output'"""
        # TODO: Consider out-phasing this and use target instead.
        return self.target

    @property
    def target(self) -> str:
        """Get the name of the output node. Does the same as 'output'"""
        return self.names[0]

    @property
    def features(self):
        """Get the name of the input features of the model. Does the same as 'inputs'"""
        return self.inputs

    @property
    def inputs(self):
        """Get the name of the input features of the model."""
        return [name for name in self.names[1:] if name != ""]

    @property
    def kind(self):
        return 'classification' if self[0].fname == 'out:lr' else 'regression'

    def save(self, file: Union[PathLike, TextIO]) -> None:
        """
        Save the `Model` to a file-like object.

        The file can later be used to recreate the `Model` with `Model.load`.

        Arguments:
            file -- A file-like object or path to save the model to.
        """

        as_dict = {
            "program": self._program.to_json(),
            "params": self.params,
            "names": self.names,
            "fnames": self.fnames,
        }

        as_dict["version"] = SCHEMA_VERSION

        if isinstance(file, (str, bytes, Path)):
            with open(file, mode="w") as f:
                json.dump(as_dict, f)
        else:
            json.dump(as_dict, file)

    @staticmethod
    def load(file: Union[PathLike, TextIO]) -> "Model":
        """
        Load a `Model` from a file.

        Usually used together with `Model.save`.

        Arguments:
            file -- A file-like object or a path to load the `Model` from.

        Returns:
            Model -- The loaded `Model`-object.
        """
        if isinstance(file, (str, bytes, Path)):
            with open(file, mode="r") as f:
                as_dict = json.load(f)
        else:
            as_dict = json.load(file)

        return Model(
            Program.from_json(as_dict["program"]),
            as_dict["names"],
            as_dict["fnames"],
            as_dict["params"],
        )

    def __hash__(self):
        return hash(self._program)

    def __eq__(self, other):
        return other.__hash__() == self.__hash__()

    def __len__(self):
        return len(self.names)

    def __iter__(self):
        return iter(self._elements)

    def __getitem__(self, ix):
        return self._elements[ix]

    def fit(self, data: DataFrame, loss_function=_feyn.DEFAULT_LOSS, sample_weights=None):
        """
        Fit this specific `Model` with the given data set.

        Arguments:
            data -- Training data including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            loss_function -- Name of the loss function or the function itself. This is the loss function to use for fitting. Can either be a string or one of the functions provided in `feyn.losses`.
            sample_weights -- An optional numpy array of weights for each sample. If present, the array must have the same size as the data set, i.e. one weight for each sample

        """

        # Magic support for pandas DataFrame
        if type(data).__name__ == "DataFrame":
            data = {col: data[col].values for col in data.columns}

        length = len(list(data.values())[0])

        # Create a sequence of indices from the permuted data of length n_samples
        permutation = np.random.permutation(length)
        data = {key: values[permutation] for key, values in data.items()}

        if sample_weights is not None:
            # Normalise the sample_weights
            sample_weights = np.multiply(list(sample_weights), 1 / max(sample_weights))
            # Also permute the sample_weights
            sample_weights = sample_weights[permutation]

        loss_function = feyn.losses._get_loss_function(loss_function)
        if not hasattr(loss_function, "c_derivative"):
            raise ValueError(
                "Loss function cannot be used for fitting, since it doesn't have a corresponding c derivative"
            )

        self._fit(data, loss_function, sample_weights)

    def _fit(self, data, loss_function, sample_weights=None, qid_to_sample_priorities=None):
        Y = data[self.target]

        self._loss = loss_function.c_derivative

        self._qepler.params = self.params

        predictions = self._qepler._query(data, Y, sample_weights)
        losses = loss_function(Y.astype(float), predictions)
        if sample_weights is not None:
            losses *= sample_weights
        if qid_to_sample_priorities is not None:
            losses *= qid_to_sample_priorities.get(self._program.qid, 1.0)

        loss_val = np.mean(losses)
        self.loss_values.append(loss_val)

        # TODO: This could be a mean of the losses collected until now
        self.loss_value = loss_val

        self._sample_count += len(Y)

        self.params = self._qepler.params

        return self.loss_value

    def _repr_svg_(self):
        return feyn._current_renderer(self)

    def _repr_html_(self):
        return feyn._current_renderer(self)

    def savefig(self, filename: str) -> str:
        """Save model as an svg file.

        Args:
            filename (str): the filename of the file to save. Includes the filepath and file extension.

        Returns:
            str: status of save operation
        """
        with open(filename, "w") as fd:
            fd.write(self._repr_svg_())

        return "Model saved successfully"

    def sympify(self, signif: int = 6, symbolic_lr=False, include_weights=True):
        """
        Convert the model to a sympy expression.
        This function requires sympy to be installed.

        Arguments:
            signif -- the number of significant digits in the parameters of the model
            symbolic_lr -- express logistic regression wrapper as part of the expression

        Returns:
            expression -- a sympy expression

        """
        return feyn.tools.sympify_model(
            self,
            signif=signif,
            symbolic_lr=symbolic_lr,
            include_weights=include_weights,
        )

    def copy(self) -> "Model":
        """Return a copy of self."""
        return Model(
            self._program.copy(), list(self.names), list(self.fnames), params=list(self.params)
        )

    def show(
        self,
        label: Optional[str] = None,
        update_display: bool = False,
        filename: Optional[str] = None,
    ):
        """Updates the display in a python notebook with the graph representation of a model

        Keyword Arguments:
            label {Optional[str]} -- A label to add to the rendering of the model (default is None).
            update_display {bool} -- Clear output and rerender figure (defaults to False).
            filename {Optional[str]} -- The filename to use for saving the plot as html (defaults to None).
        """
        feyn._svgrenderer.show_model(self, label, update_display, filename)

    def get_parameters(self, feature_name: str):
        """Given a model and the name of one of its features (input or output nodes),
        get a pandas.DataFrame with the feature's associated parameters. If the feature
        is categorical, the function returns the weight associated with each categorical
        value. If the feature is numerical, the function returns the scale, weight and
        bias.

        Arguments:
            feature_name {str} -- Name of the input or output feature of interest.

        Returns:
            pd.DataFrame -- DataFrame with the feature's parameters.
        """
        return feyn.tools.get_model_parameters(
            self,
            feature_name=feature_name
        )
