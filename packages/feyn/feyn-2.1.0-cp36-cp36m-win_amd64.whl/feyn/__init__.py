"""Feyn is the main Python module to build and execute models that utilizes a QLattice.

The QLattice stores and updates probabilistic information about the mathematical relationships (models) between observable quantities.

The workflow is typically:

# Connect to the QLattice
>>> ql = feyn.connect_qlattice()

# Extract models from the QLattice
>>> models = ql.sample_models(data.columsn, output="out")

# Fit the list of models to a local dataset
>>> models = feyn.fit_models(models, data)

# Pick the best Model from the fitted models
>>> best = models[0]

# Update the remote QLattice with this model to explore similar models.
>>> ql.update(best)

# Or use the model to make predictions
>>> predicted_y = model.predict(new_data)
"""
from ._version import _read_version, _read_git_sha
from ._model import Model
from ._qlattice import QLattice
from ._svgrenderer import show_model, _render_svg
from ._sgdtrainer import fit_models, start_performance_log, stop_and_get_performance_log
from ._qeplertrainer import fit_models as qfit_models

from ._selection import prune_models, get_diverse_models
from ._validation import validate_data

from ._qlattice import connect_qlattice

from . import tools
from . import losses
from . import criteria
from . import filters
from . import metrics
from . import plots
from . import reference
from . import datasets

_current_renderer = _render_svg
_disable_type_checks = False

__all__ = ['connect_qlattice', 'fit_models', 'prune_models', 'get_diverse_models', 'show_model', 'Model',
           'validate_data', 'QLattice']

__version__ = _read_version()
__git_sha__ = _read_git_sha()


FNAME_MAP = {
    "in:cat": {
        "paramcount": 0,
    },
    "in:linear": {
        "paramcount": 0,
    },
    "out:linear": {
        "paramcount": 0,
    },
    "out:lr": {
        "paramcount": 0,
    },

    "exp": {
        "opcode": 1000,
        "paramcount": 1,
    },
    "gaussian1": {
        "opcode": 1001,
        "paramcount": 3,
    },
    "inverse": {
        "opcode": 1002,
        "paramcount": 1,
    },
    "linear": {
        "opcode": 1003,
        "paramcount": 2,
    },
    "log": {
        "opcode": 1004,
        "paramcount": 1,
    },
    "sqrt": {
        "opcode": 1005,
        "paramcount": 1,
    },
    "squared": {
        "opcode": 1006,
        "paramcount": 1,
    },
    "tanh": {
        "opcode": 1007,
        "paramcount": 1,
    },

    "add": {
        "opcode": 2000,
        "paramcount": 1,
    },
    "gaussian2": {
        "opcode": 2001,
        "paramcount": 4,
    },
    "multiply": {
        "opcode": 2002,
        "paramcount": 2,
    },
}

OPCODE_MAP = {desc["opcode"]: fname for fname, desc in FNAME_MAP.items() if "opcode" in desc}