import numpy as np

from ._structural import _sort_by_structural_diversity
from ._clustering import _assign_qcells_by_clustering
from ._bootstrap import _assign_qcells_by_bootstrap


__all__ = [
    "_sort_by_structural_diversity",
    "_assign_qcells_by_clustering",
    "_assign_qcells_by_bootstrap",
]


def bic(loss_value: float, param_count: int, n_samples: int) -> float:
    return n_samples * np.log(loss_value) + param_count * np.log(n_samples)


def aic(loss_value: float, param_count: int, n_samples: int) -> float:
    return n_samples * np.log(loss_value) + param_count * 2
