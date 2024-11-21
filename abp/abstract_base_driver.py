"""Creating abstract builder for templating pipelines."""

from typing import Optional

import graphviz
from hamilton import driver, graph_types


class NodeTypeError(Exception):
    """Custom error to flag abstract nodes."""

    pass


def custom_style(
    *, node: graph_types.HamiltonNode, node_class: str
) -> tuple[dict[str, str], str, str]:
    """Creating display style for abstract nodes."""
    if node.tags.get("node_type") == "abstract":
        style = ({"fillcolor": "blue"}, node_class, "ABC Node")
    else:
        style = ({"fillcolor": "orange"}, node_class, "template")

    return style


class AbcBuilder(driver.Builder):
    """Abstract Builder for templating pipelines."""

    @staticmethod
    def list_abstract_nodes(dr: driver.Driver) -> list[str]:
        """Returns all nodes that are tagged abstract."""
        list_of_abstract_nodes = dr.list_available_variables(
            tag_filter={"node_type": "abstract"}
        )
        return list_of_abstract_nodes

    def build(self) -> driver.Driver:
        """Adding validation step that no nodes are abstract.

        :return: The driver you specified.
        """
        dr_candidate = super().build()
        ls_abc_nodes = AbcBuilder.list_abstract_nodes(dr_candidate)
        if ls_abc_nodes:
            raise NodeTypeError(
                "Cannot initialise DAG with abstract nodes. "
                f"Please implement the following: {ls_abc_nodes}"
            )

        return dr_candidate

    def visualize(self) -> Optional[graphviz.Digraph]:  # noqa F821
        """Display template DAG."""
        dr_candidate = super().build()
        return dr_candidate.display_all_functions(custom_style_function=custom_style)
