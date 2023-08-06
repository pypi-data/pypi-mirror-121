import numpy as np
from pandas import DataFrame, Series
import feyn

from typing import Union
from feyn._typings import check_types

from feyn.plots._svg_toolkit import SVGGraphToolkit


def _get_min_max(model, data):
    activations = feyn.metrics._metrics._get_activations(model, data)

    minval = min(0, activations.min())
    maxval = max(0, activations.max())

    return minval, maxval


@check_types()
def plot_activation_flow(model: feyn.Model, data: DataFrame, sample: Union[DataFrame, Series]):  # -> "SVG":
    """
    Plot a model of a model displaying the flow of activations.

    Arguments:
        model {feyn.Model}   -- A feyn.Model we want to describe given some data.
        data {DataFrame} -- A Pandas DataFrame to compute on.
        sample {Iterable} - The sample you want to visualize

    Raises:
        TypeError: if inputs don't match the correct type.

    Returns:
        SVG -- SVG of the model summary.
    """
    gtk = SVGGraphToolkit()

    # NOTE: Consider doing range [0,1] for classification
    # and min/max of prediction for regression to keep colors focused on output
    minmax = _get_min_max(model, data)

    model.predict(sample)
    activations = [np.round(model._qepler.activation(ix)[0], 2) for ix in range(len(model))]

    gtk.add_graph(model, label="Displaying activation of individual nodes")
    gtk.label_nodes(activations)
    gtk.color_nodes(by=activations, crange=minmax)
    gtk.add_colorbars(label="Activation strength")

    from IPython.display import HTML

    return HTML(gtk._repr_html_())
