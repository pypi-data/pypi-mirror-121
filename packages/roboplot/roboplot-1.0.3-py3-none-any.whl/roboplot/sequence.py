"""Functions to plot sequences."""

from typing import Iterable

import numpy as np
from matplotlib import pyplot as plt

from roboplot.base import (get_figure_and_axes, set_axes_equal, set_labels,
                           set_title, show_option)


@show_option
def plot_contact_sequence(values, fignum=0, colors='rgby', fig_size=(5, 1)):
    """
    
    """
    fig, axes = plt.subplots(len(values.keys()),
                             num=fignum,
                             constrained_layout=True,
                             figsize=fig_size)
    for idx, (key, value) in enumerate(values.items()):
        value = np.asarray(value)
        sequence = np.where(value > 0)[0]

        # Plot underlying dots
        axes[idx].scatter(np.arange(value.shape[0]),
                          np.zeros(value.shape),
                          marker='8',
                          s=fig_size[0])

        # Plot colored squares where contact was made
        axes[idx].scatter(sequence,
                          np.zeros(sequence.shape),
                          marker='s',
                          color=colors[idx],
                          s=60 * fig_size[0])

        axes[idx].set_ylabel(key, rotation='horizontal', va='center')

        # Turn off all axis elements except for ylabel
        # axes[idx].set_axis_off()
        axes[idx].xaxis.set_visible(False)
        axes[idx].tick_params(left=False, labelleft=False)
        #remove background patch (only needed for non-white background)
        axes[idx].patch.set_visible(False)

        # remove the box around the plot
        axes[idx].spines["right"].set_visible(False)
        axes[idx].spines["top"].set_visible(False)
        axes[idx].spines["left"].set_visible(False)
        axes[idx].spines["bottom"].set_visible(False)

    return fig


@show_option
def plot_foot_contacts(contact_points: dict,
                       fignum: int = 0,
                       title: str = "Contact Points",
                       labels: Iterable = ("X axis", "Y axis", "Z axis"),
                       colors: Iterable = 'rgby',
                       color_legend: Iterable = "rgby"):
    """
    Plot trajectory of foot contact points.

    Args:
        contact_points (dict): A dict with keys as foot indices and Tx3 matrix as values,
            where T is the number of timesteps.
        fignum (int): The figure number to plot this on.
        title (str): Title of the plot.
        colors (Iterable): Colors of each of the line plots.
        show (bool): Flag indicating whether to display the plot.

    Returns:
        A matplotlib Figure.
    """
    fig, axes = get_figure_and_axes(fignum, projection='3d')

    for idx, points in enumerate(contact_points.values()):
        axes.scatter(points[:, 0],
                     points[:, 1],
                     points[:, 2],
                     color=colors[idx],
                     label=color_legend[idx])

    set_title(fig, title)
    set_axes_equal(fig)
    set_labels(fig, labels)

    axes.legend(loc="upper right")

    return fig
