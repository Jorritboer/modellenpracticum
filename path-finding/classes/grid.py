from numpy import array
from queue import PriorityQueue
from typing import Dict, List, Optional

from .point import Point
from .rect import Rect
from .tile import Tile
from .tile_attribute import TileAttribute
from .tile_data import TileData
from ..helpers import lerp


class Grid:
    """Information of a grid of tiles useable for path finding."""

    _dimensions: Rect
    _tiles: array
    _path_finding_has_run: bool

    def __init__(self, dimensions: Rect):
        self._dimensions = dimensions
        self._tiles = array(
            [
                [Tile(Point(x, y)) for y in range(dimensions.height)]
                for x in range(dimensions.width)
            ]
        )
        self._path_finding_has_run = False

    @property
    def dimensions(self) -> Rect:
        """Get the dimensions of the grid."""
        return self._dimensions

    def _tile_at(self, pos: Point) -> Tile:
        # Get Tile in grid given Point.
        return self._tiles[pos.x, pos.y]

    def tile_data_at(self, pos: Point) -> Optional[TileData]:
        """Get TileData in grid given Point."""
        return self._tile_at(pos).data

    def register_tile_at(self, pos: Point, data: TileData) -> None:
        """Register the tile with the given tile data."""
        self._tile_at(pos).register(data)

    def deregister_tile_at(self, pos: Point) -> None:
        """Deregister the tile by removing its tile data."""
        self._tile_at(pos).deregister()

    def reset(self) -> None:
        """Reset the grid, so it can be used in another path finding computation."""
        for row in self._tiles:
            for tile in row:
                tile.reset()
        self._path_finding_has_run = False

    def _undiscover_all(self) -> None:
        # Reset all tiles' visited states to Undiscovered.
        for row in self._tiles:
            for tile in row:
                tile.undiscover()

    def _neighbours_of(self, tile: Tile) -> List[Tile]:
        # Get the up to 8 neighbours of the given tile.
        # Unregistered tiles do not count.
        return [
            self._tiles[x, y]
            for x in range(
                max(tile.pos.x - 1, 0), min(tile.pos.x + 2, self.dimensions.width)
            )
            for y in range(
                max(tile.pos.y - 1, 0), min(tile.pos.y + 2, self.dimensions.height)
            )
            if self._tiles[x, y].registered and Point(x, y) != tile.pos
        ]

    def _heuristic_of(self, tile: Tile, to_tile: Tile) -> float:
        # Get the A* heuristic for a tile.
        # Uses the given end tile for A* to calculate the heuristic with.
        return tile.pos.dist(to_tile.pos)

    def path_to(self, pos: Point) -> List[Point]:
        """
        Return the path from the starting point to the given point.
        Only valid if A* has already been run on the grid.
        """
        if not self._path_finding_has_run:
            raise Exception("Must run A* before getting a tile's path")
        return self._path_to_rec(self._tile_at(pos), [])

    def _path_to_rec(self, tile: Tile, path: List[Point] = []) -> List[Point]:
        # Recursive helper function for path, calculating a tile's path
        path.insert(0, tile.pos)
        return path if tile.parent is None else self._path_to_rec(tile.parent, path)

    def find_path(
        self, from_pos: Point, to_pos: Point, **kwargs
    ) -> Optional[List[Point]]:
        """
        Run A* on the grid.

        Calls reset() beforehand if needed.
        If no path can be found, it returns None.
        Otherwise, it returns the path.

        Optional arguments:
        max_length: float -- the maximum length of the path, default None
        path_cost: float -- the base cost of the path per length unit, default 0
        existing_paths: List[List[Point]] -- existing paths that should be weighted more, default None
        existing_path_multiplier: float -- how much more existing paths should be weighted (diminishes linearly with distance), default 1
        existing_path_radius: int -- how many tiles the existing paths stretch for purpose of weight multiplication, default 0
        attribute_multipliers: Dict[TileAttribute, float] -- weight multipliers for each TileAttribute, default 1
        """

        # Variable setup and defaults
        max_length = kwargs.get("max_length")
        path_cost = kwargs.get("path_cost") or 0
        existing_paths = kwargs.get("existing_paths")
        attribute_multipliers = kwargs.get("attribute_multipliers")

        from_tile = self._tile_at(from_pos)
        to_tile = self._tile_at(to_pos)

        # Cleanup to prepare for running the algorithm
        if self._path_finding_has_run:
            self.reset()
        self._path_finding_has_run = True

        # Correct weights to attributes
        if attribute_multipliers is not None:
            self._correct_weights_to_attributes(attribute_multipliers)

        # Corrects weights to existing_paths
        if existing_paths is not None:
            existing_path_multiplier = kwargs.get("existing_path_multiplier") or 1
            existing_path_radius = kwargs.get("existing_path_radius") or 0
            if existing_path_multiplier < 1:
                raise Exception(
                    "An existing path multiplier of less than 1 makes no sense"
                )
            if existing_path_multiplier > 1 and len(existing_paths) > 0:
                self._correct_weights_to_paths(
                    existing_paths, existing_path_multiplier, existing_path_radius
                )

        # Initialisation of A*
        to_visit = PriorityQueue()  # to_visit is a queue of (cost with heuristic, tile)
        from_tile.cost = from_tile.weight
        from_tile.path_length = 0
        to_visit.put(
            (
                from_tile.cost + from_tile.heuristic(to_tile, self._heuristic_of),
                from_tile,
            )
        )

        # Main A* loop
        while len(to_visit.queue) > 0:
            # Visit next tile
            s_cost, s_tile = to_visit.get()
            if s_tile.visited or (
                max_length is not None and s_tile.path_length >= max_length
            ):
                continue

            if s_tile.pos == to_pos:
                # We found the shortest path
                return self.path_to(s_tile.pos)

            s_tile.visit()

            # Discover neighbours
            neighbours = self._neighbours_of(s_tile)
            for c_tile in neighbours:
                # Skip neighbour if already visited
                if c_tile.visited:
                    continue

                # Calculate cost of neighbour from this parent
                dist = s_tile.pos.dist(c_tile.pos)
                c_cost = s_cost + c_tile.weight + dist * path_cost
                c_full_cost = c_cost + c_tile.heuristic(to_tile, self._heuristic_of)

                # Check if this cost is lower than any previous costs (skip neighbour if not)
                if c_tile.discovered:
                    c_full_costs = [
                        cost for (cost, tile) in to_visit.queue if tile == c_tile
                    ]
                    if c_full_cost >= min(c_full_costs):
                        continue

                # Discover neighbour
                c_tile.discover()
                c_tile.parent = s_tile
                c_tile.cost = c_cost
                c_tile.path_length = s_tile.path_length + dist
                to_visit.put((c_full_cost, c_tile))

        # No path exists
        return None

    def path_to_string(self, path: List[Point]) -> str:
        """Format a path into a human-readable string."""
        return " -> ".join([f"{pos.x},{pos.y}" for pos in path])

    def _correct_weights_to_attributes(
        self, attribute_multipliers: Dict[TileAttribute, float]
    ) -> None:
        for attribute in TileAttribute:
            if attribute_multipliers[attribute] is None:
                attribute_multipliers[attribute] = 1

        for row in self._tiles:
            for tile in row:
                if not tile.registered:
                    continue
                attributes = tile.data.get_attributes()
                for attribute in attributes:
                    tile.weight = tile.weight * attribute_multipliers[attribute]

    def _correct_weights_to_paths(
        self, paths: List[List[Point]], multiplier: int, radius: int
    ) -> None:
        to_visit = [
            (pos, 0) for path in paths for pos in path if self._tile_at(pos).registered
        ]
        for pos, _ in to_visit:
            self._tile_at(pos).visit()

        while len(to_visit) > 0:
            pos, dist = to_visit.pop(0)
            tile = self._tile_at(pos)
            tile.weight = tile.data.weight * lerp(multiplier, 1, dist / radius)
            if dist >= radius:
                continue
            neighbours = [n for n in self._neighbours_of(tile) if not n.visited]
            for neighbour in neighbours:
                neighbour.visit()
            to_visit.extend([(n.pos, dist + 1) for n in neighbours])

        self._undiscover_all()
