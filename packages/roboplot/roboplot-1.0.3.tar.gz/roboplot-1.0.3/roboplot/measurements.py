"""Classes and functions to plot sensor data."""

from typing import Iterable

import numpy as np
from matplotlib import pyplot as plt

from roboplot.base import get_figure_and_axes, multirow, set_title, show_option


@show_option
def plot_measurements(x,
                      y,
                      fignum=0,
                      xlabel="x",
                      ylabel="y",
                      color="b",
                      title="Measurements"):
    """
    Plot a set of measurements as a line graph.

    Args:
        x: The x-axis data.
        y: The y-axis data.
        fignum: The figure number to plot this on.
        xlabel: The label on the x-axis.
        ylabel: The label on the y-axis.
        color: Color of the line plot (default is blue).
        title: Title of the plot.
        show: Flag indicating whether to display the plot.

    Returns:
        A matplotlib Figure.
    """
    fig, axes = get_figure_and_axes(fignum)

    axes.plot(x, y, "tab:{}".format(color))
    axes.set(xlabel=xlabel, ylabel=ylabel)

    fig = set_title(fig, title)

    return fig


@show_option
def plot_multirow_measurements(x: Iterable,
                               y: Iterable,
                               fignum: int = 0,
                               title: str = "Multiple Measurements",
                               xlabels: Iterable[str] = None,
                               ylabels: Iterable[str] = None,
                               colors: Iterable = None,
                               row_titles: Iterable[str] = None,
                               normalize: bool = False):
    """
    Plot multiple measurements over multiple rows for easy viewing and comparisons.

    Args:
        x (Iterable): The x-axis data. Common to all y-axis data rows.
        y (Iterable): The y-axis data. This is a NxR matrix of R sets of N data points.
        fignum (int): The figure number to plot this on.
        title (str): Title of the plot.
        xlabels (Iterable[str]): The labels on the x-axis.
        ylabels (Iterable[str]): The labels on the y-axis.
        colors (Iterable): Colors of each of the line plots.
        row_titles (Iterable[str]): The title of each individual subplot.
        normalize (bool): Flag to scale both axes to be of similar range.
        show (bool): Flag indicating whether to display the plot.

    Returns:
        A matplotlib Figure.
    """
    fig = multirow(x,
                   y,
                   fignum=fignum,
                   xlabels=xlabels,
                   ylabels=ylabels,
                   title=title,
                   row_titles=row_titles,
                   colors=colors,
                   normalize=normalize,
                   show=plot_multirow_measurements.__wrapped__.show)

    return fig


def get_limits(lower, upper, padding=0.1):
    """
    Add padding to the lower and upper limits.

    Args:
        lower: Lower limit
        upper: Upper limit
        padding: The amount of padding to add as a fractional percentage [0, 1]
    """
    upper_padding = padding * upper

    if upper > 0:
        upper += upper_padding
    elif upper == 0:
        upper += padding
    else:
        upper -= upper_padding

    lower_padding = padding * lower
    if lower > 0:
        lower -= lower_padding
    elif lower == 0:
        lower -= padding
    else:
        lower += lower_padding

    return (lower, upper)


@show_option
def plot_imu_measurements(timestamps: np.ndarray,
                          angular_velocity: np.ndarray,
                          linear_acceleration: np.ndarray,
                          fignum: int = 0,
                          title: str = "IMU Measurement Data",
                          labels=('X Axis', 'Y Axis', 'Z Axis'),
                          colors=('r', 'g', 'b')):
    """
    Plot measurements from an IMU.

    Args:
        timestamps (numpy.ndarray): N-dimensional vector of time indices.
        angular_velocity (numpy.ndarray): Nx3 matrix of angular velocity measurements.
        linear_acceleration (numpy.ndarray): Nx3 matrix of linear acceleration measurements.
        fignum (int): The figure number to plot this on.
        title (str): Title of the plot.
        labels (Iterable[str]): The labels for each subplot.
        colors (Iterable): Colors of each of the line plots.
        show (bool): Flag indicating whether to display the plot.

    Returns:
        A matplotlib Figure.
    """
    fig, axes = plt.subplots(2, 3, num=fignum, constrained_layout=True)

    set_title(fig, title)

    y_min, y_max = 0, 0

    # plot angular velocity
    for i, (label, color) in enumerate(zip(labels, colors)):
        ax = axes[0][i]
        ax.plot(
            timestamps / 10**9,  # timestamps are in nanosecs
            angular_velocity[:, i],
            color=color)
        ax.set_title(label)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Angular Velocity')

        y_min, y_max = get_limits(angular_velocity[:, i].min(),
                                  angular_velocity[:, i].max(),
                                  padding=2)
        ax.set_ylim(y_min, y_max)

    # plot linear acceleration
    for i, (label, color) in enumerate(zip(labels, colors)):
        ax = axes[1][i]
        ax.plot(
            timestamps / 10**9,  # timestamps are in nanosecs
            linear_acceleration[:, i],
            color=color)
        ax.set_title(label)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Linear Acceleration (m/s²)')

        y_min, y_max = get_limits(linear_acceleration[:, i].min(),
                                  linear_acceleration[:, i].max(),
                                  padding=2)
        ax.set_ylim(y_min, y_max)

    return fig
