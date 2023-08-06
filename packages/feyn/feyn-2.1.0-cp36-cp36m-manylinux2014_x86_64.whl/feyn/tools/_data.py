"""Helper functions that may make it easier to interact with feyn."""
import numpy as np
from pandas import DataFrame
import feyn
from typing import List, Iterable


def split(data: Iterable, ratio: List[float] = [1, 1], random_state: int = None) -> List[Iterable]:
    """
    Split datasets into random subsets

    This function is used to split a dataset into random subsets - typically training and test data.

    The input dataset should be either a pandas DataFrames or a dictionary of numpy arrays. The ratio parameter controls how the data is split, and how many subsets it is split into.

    Example: Split data in the ratio 2:1 into train and test data
    >>> train, test = feyn.tools.split(data, [2,1])

    Example: Split data in to train, test and validation data. 80% training data and 10% validation and holdout data each
    >>> train, validation, holdout = feyn.tools.split(data, [.8, .1, .1])


    Arguments:
        data -- The data to split (DataFrame or dict of numpy arrays).
        ratio -- the size ratio of the resulting subsets
        random_state -- the random state of the split (integer)

    Returns:
        list of subsets -- Subsets of the dataset (same type as the input dataset).
    """

    columns = list(data.keys())
    sz = len(data[columns[0]])

    rng = np.random.default_rng(seed=random_state)
    permutation = rng.permutation(sz)
    segment_sizes = np.ceil((np.array(ratio) / sum(ratio) * sz)).astype(int)

    segment_indices = []

    start_ix = 0
    for segment_size in segment_sizes:
        end_ix = start_ix + segment_size
        segment_indices.append(permutation[start_ix:end_ix])
        start_ix = end_ix

    result = []
    for indices in segment_indices:
        if type(data).__name__ == "DataFrame":
            result.append(data.iloc[indices])
        else:
            result.append({col: coldata[indices] for col, coldata in data.items()})

    return result


def select_features(df: DataFrame, target: str, n: int = 25):
    """Selects the top N features according to mutual information

    Arguments:
        df {DataFrame} -- The dataframe to select features for.
        target {str} -- The output feature to measure against.

    Keyword Arguments:
        n {int} -- Max amount of features to include in result (default: {25}).

    Returns:
        list -- List of top features according to mutual information.
    """
    res = {}
    # Compute mutual information
    for f in df.columns:
        if f == target:
            continue
        v = df[[f, target]].values.T
        mi = feyn.metrics.calculate_mi(v, float_bins=5)
        res[f] = mi

    # Sort by mutual information
    res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}

    return list(res)[:n] + [target]


def get_feature_priors(df: DataFrame, target: str, floor: float = 0.1):
    """Calculates suitable priors for features based on mutual information.

    Arguments:
        df {DataFrame} -- The dataframe to calculate priors for.
        target {str} -- The output feature to measure against.

    Keyword Arguments:
        floor {float} -- The minimum value for the priors (default: {0.1}).

    Returns:
        dict -- a dictionary of feature names and their computed priors.
    """
    res = []
    # Compute mutual information
    for f in df.columns:
        if f == target:
            continue
        v = df[[f, target]].values.T
        mi = feyn.metrics.calculate_mi(v, float_bins=5)
        res.append(mi)

    res = np.array(res)
    res = 1 - (-res).argsort() / 100  # note: (-res).argsort() is just reverse argsort
    res[res < floor] = floor

    return dict(zip(df.columns, res))
