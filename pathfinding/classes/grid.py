import numpy as np
from queue import PriorityQueue
from typing import Dict, List, Optional, Tuple
import math

from .point import Point
from .rect import Rect
from .tile import Tile
from .tile_attribute import TileAttribute
from .tile_data import TileData
from ..helpers.math import lerp
from .visit_state import VisitState

INVALID_PARENT = (-1, -1)


def dist(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> float:
    return math.sqrt(
        (float(from_pos[0]) - float(to_pos[0])) ** 2
        + (float(from_pos[1]) - float(to_pos[1])) ** 2
    )


class Grid:
    """Information of a grid of tiles useable for path finding."""

    _dimensions: Rect
    _weights: np.ndarray
    _base_weights: np.ndarray
    _visit_states: np.ndarray
    _parents: np.ndarray
    _costs: np.ndarray
    _heuristics: np.ndarray
    _path_lengths: np.ndarray
    _attributes: np.ndarray
    _registered: np.ndarray
    _path_finding_has_run: bool

    def __init__(self, dimensions: Rect):
        self._dimensions = dimensions
        shape = (dimensions.width, dimensions.height)
        self._weights = np.zeros(shape, dtype=np.float_)
        self._base_weights = np.zeros(shape, dtype=np.float_)
        self._visit_states = np.zeros(shape, dtype=np.int8)
        self._parents = np.empty(shape, dtype=(np.int_, 2))
        self._parents[...] = INVALID_PARENT
        self._costs = np.zeros(shape, dtype=np.float_)
        self._heuristics = np.zeros(shape, dtype=np.float_)
        self._path_lengths = np.zeros(shape, dtype=np.float_)
        self._attributes = np.zeros(shape, dtype=np.int64)
        self._registered = np.zeros(shape, dtype=np.bool_)
        self._path_finding_has_run = False

    @property
    def dimensions(self) -> Rect:
        """Get the dimensions of the grid."""
        return self._dimensions

    def get_cost(self, pos: Tuple[int, int]) -> float:
        return self._costs[pos]

    def set_cost(self, pos: Tuple[int, int], value: float):
        self._costs[pos] = value

    def get_base_weight(self, pos: Tuple[int, int]) -> float:
        return self._base_weights[pos]

    def set_base_weight(self, pos: Tuple[int, int], value: float):
        self._base_weights[pos] = value

    def get_weight(self, pos: Tuple[int, int]) -> float:
        return self._weights[pos]

    def set_weight(self, pos: Tuple[int, int], value: float):
        self._weights[pos] = value

    def get_heuristic(self, pos: Tuple[int, int]) -> float:
        return self._heuristics[pos]

    def set_heuristic(self, pos: Tuple[int, int], value: float):
        self._heuristics[pos] = value

    def get_parent(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        p = self._parents[pos]
        return (p[0], p[1])

    def set_parent(self, pos: Tuple[int, int], value: Tuple[int, int]):
        self._parents[pos] = value

    def get_path_length(self, pos: Tuple[int, int]) -> float:
        return self._path_lengths[pos]

    def set_path_length(self, pos: Tuple[int, int], value: float):
        self._path_lengths[pos] = value

    def get_visit_state(self, pos: Tuple[int, int]) -> VisitState:
        return VisitState(self._visit_states[pos])

    def set_visit_state(self, pos: Tuple[int, int], value: VisitState):
        self._visit_states[pos] = value.value

    def get_registered(self, pos: Tuple[int, int]) -> bool:
        return self._registered[pos]

    def set_registered(self, pos: Tuple[int, int], value: bool):
        self._registered[pos] = value

    def get_attribute(self, pos: Tuple[int, int], attr: TileAttribute) -> bool:
        return bool(self._attributes[pos] & (1 << int(attr)))

    def set_attribute(self, pos: Tuple[int, int], attr: TileAttribute, value: bool):
        if self.get_attribute(pos, attr) != value:
            self._attributes[pos] ^= 1 << attr

    def register_tile_at(
        self,
        pos: Tuple[int, int],
        base_weight: float = 0,
        attributes: List[TileAttribute] = [],
    ) -> None:
        """Register the tile with the given tile data."""
        self.set_registered(pos, True)
        self.set_base_weight(pos, base_weight)
        self.set_weight(pos, base_weight)
        for attribute in attributes:
            self.set_attribute(pos, attribute, True)

    def deregister_tile_at(self, pos: Tuple[int, int]) -> None:
        """Deregister the tile by removing its tile data."""
        self.set_registered(pos, False)

    def reset(self) -> None:
        """Reset the grid, so it can be used in another path finding computation."""
        self._parents[...] = INVALID_PARENT
        self._costs[...] = 0
        self._heuristics[...] = 0
        self._path_lengths[...] = 0
        self._visit_states[...] = VisitState.Undiscovered.value
        self._path_finding_has_run = False

    def _undiscover_all(self) -> None:
        # Reset all tiles' visited states to Undiscovered.
        self._visit_states[...] = VisitState.Undiscovered.value

    def _neighbours_of(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        # Get the up to 8 neighbours of the given tile.
        # Unregistered tiles do not count.
        return [
            (x, y)
            for x in range(max(pos[0] - 1, 0), min(pos[0] + 2, self.dimensions.width))
            for y in range(max(pos[1] - 1, 0), min(pos[1] + 2, self.dimensions.height))
            if self._registered[x, y] and (x, y) != pos
        ]

    def _heuristic_of(
        self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], path_cost: float
    ) -> float:
        # Get the A* heuristic for a tile.
        # Uses the given end tile for A* to calculate the heuristic with.
        return path_cost * dist(from_pos, to_pos)

    def path_to(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return the path from the starting point to the given point.
        Only valid if A* has already been run on the grid.
        """
        if not self._path_finding_has_run:
            raise Exception("Must run A* before getting a tile's path")
        path = [pos]
        while not np.array_equal((pos := self.get_parent(pos)), INVALID_PARENT):
            path += [pos]
        path.reverse()
        return path

    def find_path(
        self,
        from_pos: Tuple[int, int],
        to_pos: Tuple[int, int],
        max_length=None,
        path_cost=0,
        attribute_weights=None,
        existing_paths=None,
        existing_path_multiplier=1,
        existing_path_radius=0,
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Run A* on the grid.

        Calls reset() beforehand if needed.
        If no path can be found, it returns None.
        Otherwise, it returns the path.

        Optional arguments:
        max_length: float -- the maximum length of the path, default None
        path_cost: float -- the base cost of the path per length unit, default 0
        existing_paths: List[List[Tuple[int, int]]] -- existing paths that should be weighted more, default None
        existing_path_multiplier: float -- how much more existing paths should be weighted (diminishes linearly with distance), default 1
        existing_path_radius: int -- how many tiles the existing paths stretch for purpose of weight multiplication, default 0
        attribute_weights: Dict[TileAttribute, float] -- weights for each TileAttribute, default 0
        """

        # Cleanup to prepare for running the algorithm
        if self._path_finding_has_run:
            self.reset()
        self._path_finding_has_run = True

        # Correct weights to attributes
        if attribute_weights is not None:
            self._init_weights_from_attributes(attribute_weights)

        # Corrects weights to existing_paths
        if existing_paths is not None:
            if existing_path_multiplier < 1:
                raise Exception(
                    "An existing path multiplier of less than 1 makes no sense"
                )
            if existing_path_multiplier > 1 and len(existing_paths) > 0:
                self._correct_weights_to_paths(
                    existing_paths, existing_path_multiplier, existing_path_radius
                )

        # Initialisation of A*
        to_visit = (
            PriorityQueue()
        )  # to_visit is a queue of (cost with heuristic, cost without heuristic, tile)
        self.set_cost(from_pos, 0)
        self.set_path_length(from_pos, 0)
        to_visit.put(
            (
                self.get_cost(from_pos)
                + self._heuristic_of(from_pos, to_pos, path_cost),
                self.get_cost(from_pos),
                from_pos,
            )
        )

        # Main A* loop
        while len(to_visit.queue) > 0:
            # Visit next tile
            s_full_cost, s_cost, s_pos = to_visit.get()
            if self.get_visit_state(s_pos) == VisitState.Visited or (
                max_length is not None and self.get_path_length(s_pos) >= max_length
            ):
                continue

            if s_pos == to_pos:
                # We found the shortest path
                return self.path_to(to_pos)

            self.set_visit_state(s_pos, VisitState.Visited)

            # Discover neighbours
            neighbours = self._neighbours_of(s_pos)
            for c_pos in neighbours:
                # Skip neighbour if already visited
                if self.get_visit_state(c_pos) == VisitState.Visited:
                    continue

                # Calculate cost of neighbour from this parent
                d = dist(s_pos, c_pos)
                c_cost = (
                    s_cost
                    + (self.get_weight(c_pos) + self.get_weight(s_pos)) / 2
                    + d * path_cost
                )
                c_full_cost = c_cost + self._heuristic_of(c_pos, to_pos, path_cost)

                # Check if this cost is lower than any previous costs (skip neighbour if not)
                if self.get_visit_state(c_pos) == VisitState.Discovered:
                    c_full_costs = [
                        full_cost
                        for (full_cost, cost, pos) in to_visit.queue
                        if pos == c_pos
                    ]
                    if c_full_cost >= min(c_full_costs):
                        continue

                # Discover neighbour
                self.set_visit_state(c_pos, VisitState.Discovered)
                self.set_parent(c_pos, s_pos)
                self.set_cost(c_pos, c_cost)
                self.set_path_length(c_pos, self.get_path_length(s_pos) + d)
                to_visit.put((c_full_cost, c_cost, c_pos))

        # No path exists
        return None

    def path_to_string(self, path: List[Tuple[int, int]]) -> str:
        """Format a path into a human-readable string."""
        return " -> ".join([f"{pos[0]},{pos[1]}" for pos in path])

    def _weight_from_attributes(
        self,
        pos: Tuple[int, int],
        base_weight: float,
        attribute_weights: Dict[TileAttribute, float],
    ) -> float:
        weight = base_weight
        for attribute, attribute_weight in attribute_weights.items():
            if self.get_attribute(pos, attribute):
                weight += attribute_weight
        return weight

    def _init_weights_from_attributes(
        self, attribute_weights: Dict[TileAttribute, float] = {}
    ):
        for x in range(self.dimensions.width):
            for y in range(self.dimensions.height):
                self.set_weight(
                    (x, y),
                    self._weight_from_attributes(
                        (x, y), self.get_base_weight((x, y)), attribute_weights
                    ),
                )

    def _correct_weights_to_paths(
        self, paths: List[List[Tuple[int, int]]], multiplier: int, radius: int
    ) -> None:
        to_visit = [
            (pos, 0) for path in paths for pos in path if self.get_registered(pos)
        ]
        for pos, _ in to_visit:
            self.set_visit_state(pos, VisitState.Visited)

        while len(to_visit) > 0:
            pos, dist = to_visit.pop(0)
            self.set_weight(
                pos, self.get_weight(pos) * lerp(multiplier, 1, dist / radius)
            )
            if dist >= radius:
                continue
            neighbours = [
                n
                for n in self._neighbours_of(pos)
                if not self.get_visit_state(pos) == VisitState.Visited
            ]
            for neighbour in neighbours:
                self.set_visit_state(neighbour, VisitState.Visited)
            to_visit.extend([(n, dist + 1) for n in neighbours])

        self._undiscover_all()
