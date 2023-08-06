import pandas as pd
import feyn

from feyn._typings import check_types


@check_types()
def get_model_parameters(model: feyn.Model, feature_name: str) -> pd.DataFrame:
    """Given a model and the name of one of its features (input or output nodes),
    get a pandas.DataFrame with the feature's associated parameters. If the feature
    is categorical, the function returns the weight associated with each categorical
    value. If the feature is numerical, the function returns the scale, weight and
    bias.

    Arguments:
        model {feyn.Model} -- feyn Model of interest.
        feature_name {str} -- Name of the input or output feature of interest.

    Returns:
        pd.DataFrame -- DataFrame with the feature's parameters.
    """
    if feature_name not in model.inputs+[model.output]:
        raise ValueError(
            f"{feature_name} not in model inputs or output!"
        )

    cat_list = _determine_categories(model)
    is_categorical = feature_name in cat_list

    params_df, merge_args = _determine_initial_df_and_merge_args(feature_name, is_categorical)

    suffixes = ()
    for i, elem in enumerate(model):
        if elem.name != feature_name:
            continue

        suffixes += (f'_{i}', )
        df = _params_dataframe(elem)
        params_df = pd.merge(
            params_df, df, how='outer', suffixes=suffixes, **merge_args
        )

    return params_df


def _determine_categories(model):
    return [elem.name for elem in model if 'cat' in elem.fname]


def _determine_initial_df_and_merge_args(feature_name, is_categorical):
    if is_categorical:
        initial_df = pd.DataFrame(columns=[feature_name])
        merge_args = {'on': feature_name}
    else:
        initial_df = pd.DataFrame()
        merge_args = {'left_index': True, 'right_index': True}

    return initial_df, merge_args


def _params_dataframe(elem):
    params_df = pd.DataFrame()

    if elem.fname == "in:cat":
        params_df = pd.DataFrame(
            elem.params['categories'], columns=[elem.name, 'weights']
        ).sort_values(by='weights', ascending=False, ignore_index=True)
    elif elem.fname == "in:linear" or 'out:' in elem.fname:
        params_df = pd.DataFrame(
            elem.params, index=[elem.name]
        ).T

    return params_df


