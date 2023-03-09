from typing import Callable, Optional

from .point import Point
from .tile_data import TileData
from .visit_state import VisitState


class Tile:
    """Tile information useable for path finding."""

    _pos: Point
    _data: Optional[TileData]
    _weight: Optional[float]
    _visit_state: VisitState
    _parent: Optional["Tile"]
    _cost: Optional[float]
    _heuristic: Optional[float]
    _path_length: Optional[float]
    
    def __init__(self, pos: Point):
        self._pos = pos
        self._data = None
        self._weight = None
        self.reset()

    @property
    def pos(self) -> Point:
        """Get the tile's position."""
        return self._pos

    @property
    def data(self) -> Optional[TileData]:
        """Get the tile's tile data, if it's registered."""
        return self._data

    @property
    def registered(self) -> None:
        """Check if the tile is registered."""
        return self._data is not None

    def register(self, data: TileData) -> None:
        """Register the tile with the given tile data."""
        self._data = data
        self._weight = data.weight

    def deregister(self) -> None:
        """Deregister the tile by removing its tile data."""
        self._data = None
        self._weight = None

    @property
    def weight(self) -> Optional[float]:
        """Get the tile's corrected weight."""
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        """
        Set the tile's corrected weight.
        
        May only be called if the tile is registered.
        """
        if not self.registered():
            raise Exception("Cannot update weight for deregistered tile")
        self._weight = value

    @property
    def visited(self) -> bool:
        """Check if the tile has been visited during path finding."""
        return self._visit_state == VisitState.Visited

    @property
    def discovered(self) -> bool:
        """Check if the tile has been discovered (or even visited) during path finding."""
        return self._visit_state != VisitState.Undiscovered
    

    def visit(self) -> None:
        """Upgrade the tile to be visited."""
        self._visit_state = VisitState.Visited

    def discover(self) -> None:
        """Upgrade the tile to be discovered."""
        if not self.visited:
            self._visit_state = VisitState.Discovered

    def undiscover(self) -> None:
        """Downgrade the tile to be undiscovered."""
        self._visit_state = VisitState.Undiscovered

    @property
    def parent(self) -> Optional["Tile"]:
        """Get the tile's parent."""
        return self._parent

    @parent.setter
    def parent(self, value: "Tile") -> None:
        """Set the tile's parent."""
        self._parent = value

    @property
    def cost(self) -> Optional[float]:
        """Get the tile's base cost (i.e. without heuristic)."""
        return self._cost

    @cost.setter
    def cost(self, value: float) -> None:
        """Set the tile's base cost (i.e. without heuristic)."""
        self._cost = value

    def heuristic(self, to: "Tile", h: Callable[["Tile", "Tile"], float]) -> float:
        """
        Get the tile's heuristic, computing it if not done so yet.

        During path finding, the 'to' and 'h' arguments must be consistent.
        """
        if self._heuristic is None:
            self._heuristic = h(self, to)
        return self._heuristic

    @property
    def path_length(self) -> Optional[float]:
        """Get the tile's path length."""
        return self._path_length

    @path_length.setter
    def path_length(self, value: float) -> None:
        """Set the tile's path length."""
        self._path_length = value

    def reset(self) -> None:
        """Reset the tile, so it can be used in another path finding computation."""
        self._visit_state = VisitState.Undiscovered
        self._parent = None
        self._cost = None
        self._heuristic = None
        self._path_length = None

    def __lt__(self, other):
        return True

    def __str__(self):
        return str(self.pos)
