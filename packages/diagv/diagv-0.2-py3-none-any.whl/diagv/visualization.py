"""Functionality to visualize apps"""

from __future__ import annotations

import itertools
from collections import Mapping
from typing import Callable, Iterable, Iterator, Optional, Sequence

import more_itertools
import networkx as nx
import numpy as np
from numpy.typing import NDArray

from diagv.typing_utils import AdjacencyListT, HashableT, NormalizedAdjacencyList


def text_art(
    digraph: nx.DiGraph,
    ordering: Optional[Sequence[HashableT]] = None,
    fmt: Callable[[HashableT], str] = str,
) -> str:
    try:
        nx.find_cycle(digraph)
    except nx.NetworkXNoCycle:
        pass
    else:
        NotImplementedError("Only DAGs are supported so far")

    if ordering is None:
        ordering = list(nx.topological_sort(digraph))

    cells = _cells(digraph, ordering)
    return "".join(_fmt_cells(cells, fmt))


def _nodes(graph: AdjacencyListT[HashableT]) -> Iterator[HashableT]:
    """Yield nodes in graph in reproducible order"""
    return more_itertools.unique_everseen(itertools.chain(graph, *graph.values()))


def _inverted(
    graph: AdjacencyListT[HashableT],
) -> NormalizedAdjacencyList[HashableT]:
    """Return graph with all arrows reverted"""
    result: NormalizedAdjacencyList[HashableT] = {node: set() for node in _nodes(graph)}
    for node in result:
        for adjacent in graph.get(node, []):
            result[adjacent].add(node)
    return result


def _above_has_successor_to_the_right(
    row: int,
    col: int,
    successor_lists: Mapping[int, Iterable[int]],
) -> Optional[int]:
    successors = itertools.chain.from_iterable(
        successor_lists.get(predecessor, []) for predecessor in range(row)
    )
    try:
        return col < max(successors)
    except ValueError:
        return False


def _above_has_dpred_to_the_right(
    row: int,
    col: int,
    dpred_lists: Mapping[int, Iterable[int]],
) -> bool:
    predecessors = dpred_lists[col]
    return bool(predecessors and row < max(predecessors))


def _has_successor_to_the_right(
    col: int,
    successor_lists: Mapping[int, Iterable[int]],
) -> bool:
    successors = successor_lists[col]
    return col < max(successors, default=col)


def _has_successor_to_the_left(
    col: int,
    successor_lists: Mapping[int, Iterable[int]],
) -> bool:
    successors = successor_lists[col]
    return max(successors, default=col) < col


def _right_has_dsucc_before_this(
    row: int,
    col: int,
    dsucc_lists: Mapping[int, Iterable[int]],
) -> bool:
    dsuccs = dsucc_lists[row]
    return bool(dsuccs and min(dsuccs) <= col)


def _should_strip_left(
    col: int,
    dpred_lists: Mapping[int, Iterable[int]],
) -> bool:
    return col == 0 and not dpred_lists[0]


class Token(str):
    ...


SECTION = Token("-")
INTERSECTION = Token("+")
OVERPASS = Token("|")
PADDING = Token(" ")
NOTHING = Token("")


def _cells(digraph: nx.DiGraph, order: Sequence[HashableT]) -> NDArray:
    node2position = {v: i for i, v in enumerate(order)}
    predecessor_lists = {
        node2position[node]: [
            node2position[direct_predecessor]
            for direct_predecessor in direct_predecessors
        ]
        for node, direct_predecessors in digraph.pred.items()
    }
    successor_lists = _inverted(predecessor_lists)
    num_row = len(order)
    num_col = 4 * len(order)
    result: NDArray = np.ndarray((num_row, num_col), dtype=object)
    for row in range(num_row):
        for col in range(num_col):
            result[row, col] = "*"
    for i, row_node in enumerate(order):
        successors = set(digraph.successors(row_node))
        row = i
        for j, col_node in enumerate(order):
            predecessors = set(digraph.predecessors(col_node))
            col = j * 4
            if j < i:
                if _should_strip_left(j, predecessor_lists):
                    result[row, col + 0] = NOTHING
                elif col_node in successors:
                    result[row, col + 0] = INTERSECTION
                elif _above_has_dpred_to_the_right(i, j, predecessor_lists):
                    result[row, col + 0] = OVERPASS
                elif _right_has_dsucc_before_this(i, j, successor_lists):
                    result[row, col + 0] = SECTION
                else:
                    result[row, col + 0] = PADDING

                if _should_strip_left(j, predecessor_lists):
                    result[row, col + 1] = NOTHING
                elif _right_has_dsucc_before_this(i, j, successor_lists):
                    result[row, col + 1] = SECTION
                else:
                    result[row, col + 1] = PADDING

                if _right_has_dsucc_before_this(i, j, successor_lists):
                    result[row, col + 2] = SECTION
                    result[row, col + 3] = SECTION
                else:
                    result[row, col + 2] = PADDING
                    result[row, col + 3] = PADDING

            elif i == j:
                node = row_node
                assert node == col_node
                if _should_strip_left(j, predecessor_lists):
                    result[row, col + 0] = NOTHING
                    result[row, col + 1] = NOTHING
                elif predecessors or _has_successor_to_the_left(j, successor_lists):
                    if predecessors:
                        result[row, col + 0] = INTERSECTION
                    else:
                        result[row, col + 0] = SECTION
                    result[row, col + 1] = SECTION
                elif _above_has_successor_to_the_right(i, j, successor_lists):
                    result[row, col + 0] = PADDING
                    result[row, col + 1] = PADDING

                result[row, col + 2] = node

                if _has_successor_to_the_right(j, successor_lists):
                    result[row, col + 3] = SECTION
                # elif _has_successor_to_the_left(j, successor_lists):
                #     result[row, col + 3] = SECTION
                elif _above_has_successor_to_the_right(i, j, successor_lists):
                    result[row, col + 3] = PADDING
                else:
                    result[row, col + 3] = NOTHING
            else:
                if _should_strip_left(j, predecessor_lists):
                    result[row, col + 0] = NOTHING
                elif row_node in predecessors:
                    result[row, col + 0] = INTERSECTION
                elif (
                    predecessors
                    and min(map(node2position.__getitem__, predecessors)) < i
                ):
                    result[row, col + 0] = OVERPASS
                elif successors and j < max(map(node2position.__getitem__, successors)):
                    result[row, col + 0] = SECTION
                elif _above_has_successor_to_the_right(i, j, successor_lists):
                    result[row, col + 0] = PADDING
                else:
                    result[row, col + 0] = NOTHING

                if _should_strip_left(j, predecessor_lists):
                    result[row, col + 1] = NOTHING
                elif successors and j < max(map(node2position.__getitem__, successors)):
                    result[row, col + 1] = SECTION
                elif _above_has_successor_to_the_right(i, j, successor_lists):
                    result[row, col + 1] = PADDING
                else:
                    result[row, col + 1] = NOTHING

                if successors and j < max(map(node2position.__getitem__, successors)):
                    result[row, col + 2] = SECTION
                    result[row, col + 3] = SECTION
                elif _above_has_successor_to_the_right(i, j, successor_lists):
                    result[row, col + 2] = PADDING
                    result[row, col + 3] = PADDING
                else:
                    result[row, col + 2] = NOTHING
                    result[row, col + 3] = NOTHING

    return result


def _fmt_cells(cells: NDArray, fmt: Callable[[HashableT], str]) -> Iterator[str]:
    num_row, num_col = cells.shape
    col2width = {
        4 * row + 2: len(fmt(cells[row, 4 * row + 2])) for row in range(num_row)
    }
    for row in range(num_row):
        if row:
            yield "\n"
        for col in range(num_col):
            cell = cells[row, col]
            width = col2width.get(col, 1)
            if cell is NOTHING:
                yield ""
            elif cell in {PADDING, SECTION}:
                yield cell * width
            elif cell in {INTERSECTION, OVERPASS}:
                assert width == 1
                yield cell
            else:
                yield f"{fmt(cell)[:width]:.^{width}}"
