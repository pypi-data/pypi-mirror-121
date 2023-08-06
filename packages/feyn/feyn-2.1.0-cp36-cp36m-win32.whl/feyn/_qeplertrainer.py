import numpy as np
import itertools
import threading
from typing import Callable, Union, Optional, List, Iterable

import _feyn
import feyn

from pandas import DataFrame

from feyn._typings import check_types

@check_types()
def fit_models(
    models: List[feyn.Model],
    data: DataFrame,
    loss_function: Union[str, Callable] = _feyn.DEFAULT_LOSS,
    criterion: Optional[str] = None,
    n_samples: Optional[int] = None,
    sample_weights: Optional[Iterable[float]] = None,
) -> List[feyn.Model]:
    import qepler

    if len(models) == 0:
        return models

    # Magic support for pandas DataFrame
    data = {col: data[col].values for col in data.columns}

    length = len(next(iter(data.values())))

    if n_samples is None:
        n_samples = max(10000, length)
    if n_samples <= 0:
        raise ValueError("More than 0 samples are required for fitting models.")

    # Create a sequence of indices from the permutated data of length n_samples
    permutation = np.random.permutation(n_samples) % length
    data = {key: values[permutation] for key, values in data.items()}

    if sample_weights is not None:
        # Scale the sample_weights
        sample_weights = np.multiply(list(sample_weights), 1 / max(sample_weights))
        s_size = len(sample_weights)
        if not s_size == length:
            raise ValueError(
                f"The sizes of data ({length}) and sample_weights ({s_size}) do not match."
            )

        # Also permutate the sample_weights
        sample_weights = sample_weights[permutation]

    loss_function = feyn.losses._get_loss_function(loss_function)
    if not hasattr(loss_function, "c_derivative"):
        raise ValueError(
            "Loss function cannot be used for fitting, since it doesn't have a corresponding c derivative"
        )

    models = qepler.fit_models(models, data, loss_function, n_samples, sample_weights)

    # Remove any models that dont work for the input domain
    models = list(filter(lambda m: np.isfinite(m.loss_value), models))

    for m in models:
        m.bic = feyn.criteria.bic(m.loss_value, m._paramcount, length)
        m.aic = feyn.criteria.aic(m.loss_value, m._paramcount, length)

    if criterion == "bic":
        models.sort(key=lambda m: m.bic, reverse=False)
    elif criterion == "aic":
        models.sort(key=lambda m: m.aic, reverse=False)
    elif criterion is None:
        models.sort(key=lambda m: m.loss_value, reverse=False)
    else:
        raise Exception(
            "Unknown information criterion %s. Must be 'aic', 'bic' or None)"
            % criterion
        )

    for m in models:
        m.age += 1

    return models
