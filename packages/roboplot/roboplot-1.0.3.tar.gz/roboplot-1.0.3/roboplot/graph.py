"""
Code to plot publication-quality bayes nets and factor graphs.
"""
from typing import Iterable, Tuple, Dict

import daft
import gtsam

from roboplot.base import show_option


def get_factors_and_edges(graph):
    factors = []
    edges = []
    for idx in range(graph.nrFactors()):
        name = "f{0}".format(idx)
        factor = dict(name=name, label="", x=2 * idx, y=1)
        factors.append(factor)

        f = graph.at(idx)
        keys = f.keys()
        for key in keys:
            node = "{0}{1}".format(gtsam.symbolChr(key),
                                   gtsam.symbolIndex(key))
            edge = (node, name)
            edges.append(edge)

    return factors, edges


def get_nodes(values):
    nodes = []
    keys = values.keys()
    for idx, key in enumerate(keys):
        name = "{0}{1}".format(gtsam.symbolChr(key), gtsam.symbolIndex(key))
        label = "{0}_{1}".format(chr(gtsam.symbolChr(key)),
                                 gtsam.symbolIndex(key))
        node = dict(name=name, label="${0}$".format(label), x=2 * idx, y=0)
        nodes.append(node)

    return nodes


def _plot_bayes_net(nodes: Iterable[dict], edges: Iterable[Tuple]):
    """
    Helper function to plot a Bayes Net using Daft.

    Args:
        nodes: List of dicts defining each node of the graph.
        edges: List of 2-tuples specifying the edges between nodes.

    Returns:
        A PGM object.
    """
    G = daft.PGM(directed=True)

    for node in nodes:
        G.add_node(node["name"],
                   content=node["label"],
                   x=node["x"],
                   y=node["y"],
                   aspect=1.5)

    # merge edges for common factors
    factors = {}
    for edge in edges:
        if edge[1] in factors.keys():
            factors[edge[1]].append(edge[0])
        else:
            factors[edge[1]] = [edge[0]]

    for _, edge in factors.items():
        # These are edges to unitary factors
        if len(edge) < 2:
            continue

        G.add_edge(edge[0], edge[1])

    return G


@show_option
def plot_bayes_net(graph: gtsam.NonlinearFactorGraph,
                   values: gtsam.Values,
                   title: str = "Bayes Net") -> daft.PGM:
    """
    Plot a Bayes Net.

    *Note* that this function does not perform checks for existence of edges or nodes.

    Args:
        graph (gtsam.NonlinearFactorGraph): A factor graph which will be converted to a bayes net.
        values (gtsam.Values): A values dict.
        title (str): Plot title.
        show (bool): Flag indicating whether to display the plot.

    Returns:
        A daft PGM object.
    """
    # Get the factor and the edges
    _, edges = get_factors_and_edges(graph)

    # Get all the nodes of the graph
    nodes = get_nodes(values)

    G = _plot_bayes_net(nodes, edges)

    G.figure.suptitle(title)
    G.figure.canvas.manager.set_window_title(title.lower())

    # Set the `show_func` function so that the decorator calls it correctly.
    plot_bayes_net.__wrapped__.show_func = G.show

    G.render()

    return G


def _plot_factor_graph(nodes: Iterable[Dict], factors: Iterable[Dict],
                       edges: Iterable[Tuple]) -> daft.PGM:
    """
    Helper function to plot a factor graph using Daft.

    Args:
        nodes: List of dicts defining each node of the graph.
        factors: List of dicts defining each factor.
        edges: List of 2-tuples specifying the edges between nodes.

    Returns:
        A PGM object.
    """
    G = daft.PGM(directed=False)

    for node in nodes:
        G.add_node(node["name"],
                   content=node["label"],
                   x=node["x"],
                   y=node["y"],
                   aspect=1)

    for factor in factors:
        G.add_node(factor["name"],
                   content=factor["label"],
                   x=factor["x"],
                   y=factor["y"],
                   shape="rectangle",
                   scale=0.4,
                   plot_params={"fc": "black"})

    for edge in edges:
        G.add_edge(edge[0], edge[1])

    return G


@show_option
def plot_factor_graph(graph: gtsam.NonlinearFactorGraph,
                      values: gtsam.Values,
                      title: str = "Factor Graph") -> daft.PGM:
    """
    Plot a Factor Graph.

    *Note* that this function does not perform checks for existence of edges or nodes.

    Args:
        graph (gtsam.NonlinearFactorGraph): A factor graph.
        values (gtsam.Values): A values dict.
        title (str): Plot title.
        show (bool): Flag indicating whether to display the plot.

    Returns:
        A daft PGM object.
    """
    # Get the factor and the edges
    factors, edges = get_factors_and_edges(graph)

    # Get all the nodes of the graph
    nodes = get_nodes(values)

    G = _plot_factor_graph(nodes, factors, edges)

    G.figure.suptitle(title)
    G.figure.canvas.manager.set_window_title(title.lower())

    # Set the `show_func` function so that the decorator calls it correctly.
    plot_factor_graph.__wrapped__.show_func = G.show

    G.render()

    return G
