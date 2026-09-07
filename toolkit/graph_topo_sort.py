"""Topological sorting for directed graphs."""

from collections import deque
from collections.abc import Hashable, Mapping, Sequence
from typing import TypeVar


Node = TypeVar("Node", bound=Hashable)


def topological_sort(graph: Mapping[Node, Sequence[Node]]) -> list[Node]:
    """Return a topological ordering of *graph* using Kahn's algorithm.

    Nodes that occur only as neighbors are included in the result. A
    ``ValueError`` is raised when the graph contains a directed cycle.
    """
    in_degree: dict[Node, int] = dict.fromkeys(graph, 0)

    for neighbors in graph.values():
        for neighbor in neighbors:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

    ready = deque(node for node, degree in in_degree.items() if degree == 0)
    order: list[Node] = []

    while ready:
        node = ready.popleft()
        order.append(node)
        for neighbor in graph.get(node, ()):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                ready.append(neighbor)

    if len(order) != len(in_degree):
        raise ValueError("graph contains a cycle; topological sort is impossible")

    return order
