import gtdynamics
import matplotlib.pyplot as plt
import numpy as np

from roboplot.base import (get_figure_and_axes, set_axes_equal, set_title,
                           show_option)
from roboplot.trajectory.three_d import plot_pose3


def _dfs(robot, link_name):
    """Perform Depth-First-Search to get the robot tree."""
    link = robot.link(link_name)

    # append key type so there is no overwriting
    link_name += "_linkkey"

    node = {}
    node[link_name] = {}

    joints = link.joints()
    for j in joints:
        childLink = robot.joint(j.name()).child()

        if childLink.name() == link.name():
            continue

        # append key type so there is no overwriting
        joint_name = j.name() + "_jointkey"

        node[link_name][joint_name] = _dfs(robot, childLink.name())

    return node


@show_option
def plot_robot(robot: gtdynamics.Robot,
               root_link: str,
               fignum: int = 0,
               title: str = ""):
    """
    Plot the robot joints with connected links. Allows for visualizing robot models.

    Args:
        robot: The robot model as defined in GTDynamics.
        root_link: The base link in the provided robot.
        fignum: The figure number to plot on.
        title: The title of the plot.
        show: Flag indicating whether to display the plot.
    """

    # Generate the tree of links and joints via a Depth-First Search.
    robotTree = _dfs(robot, root_link)

    # Plot the base link frame.
    base = robot.link(root_link)
    plot_pose3(base.bMcom(), fignum=fignum)

    def _preorder(tree, key):
        """
        Traverse robot tree in pre-order format to plot the joints.
        
        We traverse over links so we can get the connections between joints.

        Args:
            tree: The result of running DFS on the robot.
            key: The node key to start traversal from.
        """
        if "_linkkey" in key:
            link = robot.link(key.replace("_linkkey", ""))

            xs, ys, zs = [], [], []

            for joint in link.joints():
                # If the joint's parent is the root link, add a connection to it.
                if joint.parent().name() == root_link:
                    xs.append(base.bMcom().translation()[0])
                    ys.append(base.bMcom().translation()[1])
                    zs.append(base.bMcom().translation()[2])

                # Compute joint's wTj using the parent link's bMcom
                # and the relation between the link and its parent.
                wTj = joint.parent().bMcom() * joint.jMp().inverse()

                xs.append(wTj.translation()[0])
                ys.append(wTj.translation()[1])
                zs.append(wTj.translation()[2])
                plot_pose3(wTj, fignum=fignum, axis_length=0.05)

            plt.plot(xs, ys, zs, "-k")

        child_keys = tree[key].keys()
        for child_key in child_keys:
            _preorder(tree[key], child_key)

    # Run _preorder traversal to plot the links correctly
    _preorder(robotTree, root_link + "_linkkey")

    # Set the axes to be proportional
    set_axes_equal(fignum)

    # Set the figure and window titles
    fig = set_title(fignum, title)

    return fig


@show_option
def plot_links(robot: gtdynamics.Robot,
               root_link: str,
               connect_links=True,
               fignum: int = 0,
               title: str = ""):
    """
    Plot only the links of the `robot`.

    Args:
        robot: The robot model as defined in GTDynamics.
        root_link: The base link in the provided robot.
        fignum: The figure number to plot on.
        title: The title of the plot.
        show: Flag indicating whether to display the plot.
    """
    for link in robot.links():
        if link.name() == root_link:
            plot_pose3(link.bMcom(), fignum=fignum)
        else:
            plot_pose3(link.bMcom(), fignum=fignum, axis_length=0.05)

    if connect_links:
        for joint in robot.joints():
            p = joint.parent().bMcom().translation()
            c = joint.child().bMcom().translation()
            _, axes = get_figure_and_axes(fignum, projection='3d')
            line = np.append(p[np.newaxis], c[np.newaxis], axis=0)
            axes.plot(line[:, 0], line[:, 1], line[:, 2])

    # Set the axes to be proportional
    set_axes_equal(fignum)

    # Set the figure and window titles
    fig = set_title(fignum, title)
