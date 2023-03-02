from numpy import array
from queue import PriorityQueue
from typing import List, Optional

from .point import Point
from .rect import Rect
from .tile import Tile
from .tile_data import TileData


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

    def register_tile_at(self, pos: Point, data: TileData) -> None:
        """Register the tile with the given tile data."""
        self._tiles[pos.x, pos.y].register(data)

    def deregister_tile_at(self, pos: Point) -> None:
        """Deregister the tile by removing its tile data."""
        self._tiles[pos.x, pos.y].deregister()

    def reset(self) -> None:
        """Reset the grid, so it can be used in another path finding computation."""
        for row in self.tiles:
            for tile in row:
                tile.reset()
        self._path_finding_has_run = False

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

    def path_to(self, pos: Point) -> [Point]:
        """
        Return the path from the starting point to the given point.
        Only valid if A* has already been run on the grid.
        """
        if not self._path_finding_has_run:
            raise Exception("Must run A* before getting a tile's path")
        return self._path_to_rec(self._tiles[pos.x, pos.y], [])

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
        """
        max_length = kwargs.get("max_length")
        path_cost = kwargs.get("path_cost") or 0
        from_tile = self._tiles[from_pos.x, from_pos.y]
        to_tile = self._tiles[to_pos.x, to_pos.y]

        if self._path_finding_has_run:
            self.reset()
        else:
            self._path_finding_has_run = True

        # Queue of (cost with heuristic, tile)
        to_visit = PriorityQueue()
        from_tile.cost = from_tile.data.weight
        from_tile.path_length = 0
        to_visit.put(
            (
                from_tile.cost + from_tile.heuristic(to_tile, self._heuristic_of),
                from_tile,
            )
        )

        while True:
            if len(to_visit.queue) == 0:
                return None

            s_cost, s_tile = to_visit.get()
            if s_tile.visited or (
                max_length is not None and s_tile.path_length >= max_length
            ):
                continue
            if s_tile.pos == to_pos:
                return self.path_to(s_tile.pos)
            s_tile.visit()

            neighbours = self._neighbours_of(s_tile)
            for c_tile in neighbours:
                dist = s_tile.pos.dist(c_tile.pos)
                c_cost = s_cost + c_tile.data.weight + dist * path_cost
                c_full_cost = c_cost + c_tile.heuristic(to_tile, self._heuristic_of)
                if c_tile.visited:
                    continue
                if c_tile.discovered:
                    c_full_costs = [
                        cost for (cost, tile) in to_visit.queue if tile == c_tile
                    ]
                    if c_full_cost >= min(c_full_costs):
                        continue
                c_tile.discover()
                c_tile.parent = s_tile
                c_tile.cost = c_cost
                c_tile.path_length = s_tile.path_length + dist
                to_visit.put((c_full_cost, c_tile))
