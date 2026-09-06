"""Tests for Kahn's algorithm topological sort."""

import pytest

from toolkit.graph_topo_sort import topological_sort


def test_diamond_dag_respects_every_edge() -> None:
    graph = {"start": ["left", "right"], "left": ["end"], "right": ["end"]}

    order = topological_sort(graph)

    positions = {node: index for index, node in enumerate(order)}
    assert set(order) == {"start", "left", "right", "end"}
    assert positions["start"] < positions["left"] < positions["end"]
    assert positions["start"] < positions["right"] < positions["end"]


def test_isolated_node_is_included() -> None:
    graph = {"before": ["after"], "isolated": []}

    order = topological_sort(graph)

    assert set(order) == {"before", "after", "isolated"}
    assert order.index("before") < order.index("after")


def test_cycle_raises_clear_exception() -> None:
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}

    with pytest.raises(ValueError, match="cycle"):
        topological_sort(graph)
