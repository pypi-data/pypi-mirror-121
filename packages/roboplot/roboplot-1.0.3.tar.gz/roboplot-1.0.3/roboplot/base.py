"""
Basic building blocks for plotting.
"""
import inspect
from operator import ge
import sys
from collections import namedtuple
from typing import Iterable, Union

import numpy as np
import wrapt
from matplotlib import pyplot as plt

# Ignore warnings from dependencies.
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def argspec_factory(wrapped):
    """Update the method signature of `wrapped`."""
    argspec = inspect.getfullargspec(wrapped)

    # Hack to add the "show" arg to the function signature
    args_dict = argspec._asdict()
    args_dict["args"].append("show")
    if args_dict["defaults"]:
        args_dict["defaults"] = tuple([*args_dict["defaults"], False])

    argspec = namedtuple('FullArgSpec',
                         args_dict.keys())._make(args_dict.values())

    new_argspec = inspect.FullArgSpec(argspec.args, argspec.varargs,
                                      argspec.varkw, argspec.defaults,
                                      argspec.kwonlyargs,
                                      argspec.kwonlydefaults,
                                      argspec.annotations)
    return new_argspec


def _arguments(*args, show=False, **kwargs):
    """
    Function to extract the `show` parameter.

    If `show` is not passed, it defaults to False.
    """
    return show, args, kwargs


def show_option(func):
    """
    Decorator to provide a default `show` option in the parameter list.

    Usages example:
    ```
    @show_option
    def plot_func():
        ...

    plot_func(show=True)
    ```

    If a plotting function is attached to an object instantiated in the function,
    you can set it as the `show_func` via this neat trick:
    ```
    @show_option
    def plot_axis():
        _, axis = plt.figure(1)
        plot_axis2.__wrapped__.show_func = axis.show
    ```

    Alternatively, you can also nest functions
    ```
    @show_option
    def plot_stream():
        ...

    @show_option
    def plot_rivers():
        plot_stream(show=plot_rivers.__wrapped__.show)

    plot_rivers(show=True)
    ```
    """
    @wrapt.decorator(adapter=argspec_factory(func))
    def _show_option(func, instance, args, kwargs):

        show, args, kwargs = _arguments(*args, **kwargs)

        # Attach the boolean flag so it is available downstream.
        func.show = show
        # Call the function.
        ret = func(*args, **kwargs)
        if show:
            if hasattr(func, "show_func"):
                # Check if custom show function is attached.
                func.show_func()
            else:
                # default to matplotlib's plt.show()
                plt.show()

        return ret

    return _show_option(func)


def get_figure(func):
    """
    Decorator to get the figure if a figure number is passed in instead of a Figure object.
    The figure parameter is required to be the first non-keyword argument.
    """
    def wrapper(*args, **kwargs):
        fig = args[0]
        if isinstance(fig, int):
            fig = plt.figure(fig)
        elif not isinstance(fig, plt.Figure):
            raise ValueError("Argument fig is not a valid Figure")

        args = tuple([fig] + list(args[1:]))
        return func(*args, **kwargs)

    return wrapper


@get_figure
def set_axes_equal(fig: Union[int, plt.Figure]):
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Args:
      fignum (int): An integer representing the figure number for Matplotlib.
    """
    ax = fig.gca()

    #TODO(Varun) Support both 3d and 2d plots correctly
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])

    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))

    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])

    return fig, ax


@get_figure
def set_labels(fig: Union[int, plt.Figure], labels: Iterable):
    """
    Set the labels for each axis of the figure.

    Args:
        fig: Matplotlib figure or figure number.
        labels: Sequence of 2/3 strings depending number of axes.
    """
    axes = fig.gca()
    if len(labels) == 3:
        axes.set_zlabel(labels[2])

    axes.set_xlabel(labels[0])
    axes.set_ylabel(labels[1])


@get_figure
def set_title(fig: Union[int, plt.Figure], title: str) -> plt.Figure:
    """
    Set the title to the figure and the window indicated by `fig`.

    Args:
        fig: Matplotlib figure or figure number.
        title: The title string to set.

    Return:
        The figure with the title and window title set.
    """
    fig.suptitle(title)
    fig.canvas.manager.set_window_title(title.lower())
    return fig


def get_figure_and_axes(fignum: int, projection=None):
    """
    Get a figure specified by fignum along with its axes.
    If the figure already has an axes, then return it else create the axes.

    Args:
        fignum: The figure number.
        projection: Type of projection. '3d' if we want 3D plots.

    Returns:
        A tuple of figure and axes.
    """
    fig = plt.figure(fignum)
    if not fig.axes:
        axes = fig.add_subplot(projection=projection)
    else:
        axes = fig.axes[0]

    return fig, axes


@show_option
def multirow(x,
             y,
             fignum=0,
             xlabels=None,
             ylabels=None,
             title="",
             row_titles=None,
             colors=("tab:blue", "tab:green", "tab:orange"),
             normalize=False) -> plt.Figure:
    """
    Make a multi-row plot.

    Useful for comparing values such as measurements from in different axes.

    Args:
        x (numpy.ndarray): Iterable of x-axis values, common to all y-axes.
        y (numpy.ndarray): Iterable of y-axis values where the first axis are the data points and the second axis is the number of rows.
        fignum (int): Matplotlib figure number.
        xlabels (iterable[string]): The labels to apply on each row's x-axis.
        ylabels (iterable[string]): The labels to apply on each row's y-axis.
        title (string): The title of the plot.
        row_titles (iterable[string]): The sub-title for each row.
        colors (iterable[string]): The color of the plot on each row.
        normalize (bool): Flag indicating whether to make the scale of the x and y axes equivalent.
        show (bool): Flag indicating whether to display the plot.
    """
    num_rows = y.shape[1]

    fig = plt.figure(fignum)
    axes = fig.subplots(num_rows, 1)

    assert num_rows == len(colors), \
        "Not enough colors provided, expected {1}, got {0}".format(len(colors),
                                                                   num_rows)

    for i in range(num_rows):
        axes[i].plot(x, y[:, i], color=colors[i])
        if row_titles:
            axes[i].set_title(row_titles[i])

        xlabel = xlabels[i] if xlabels else "x"
        ylabel = ylabels[i] if ylabels else "y"
        axes[i].set(xlabel=xlabel, ylabel=ylabel)

        if normalize:
            limits = np.array([axes[i].get_xlim(), axes[i].get_ylim()])

            origin = np.mean(limits, axis=1)
            radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))

            # axes[i].set_xlim([origin[0] - radius, origin[0] + radius])
            axes[i].set_ylim([origin[1] - radius, origin[1] + radius])

    plt.subplots_adjust(left=None,
                        bottom=None,
                        right=None,
                        top=None,
                        wspace=None,
                        hspace=1.0)

    title = title if title else "figure"
    fig = set_title(fig, title)

    return fig
