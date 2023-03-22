from typing import List
import struct

from .tile_attribute import TileAttribute


class TileData:
    """Holds generic information on tiles."""

    _weight: float
    _attributes: float

    def __init__(self, **kwargs):
        """
        Optional arguments:
        weight: float -- base cost of the tile, default 0
        attributes: List[TileAttribute] -- attributes of the tile
        """
        self._weight = kwargs.get("weight") or 0
        attributelist = set(kwargs.get("attributes") or [])
        self._attributes = float(0)
        for attributenr in attributelist:
            self._attributes += 1<<attributenr

    @property
    def weight(self) -> float:
        """Get the tile's base cost."""
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        """Set the tile's base cost."""
        self._weight = value

    def set_attribute(self, attribute: TileAttribute) -> None:
        """Set a tile attribute."""
        self._attributes += 1<<attribute

    def set_attributes(self, *attributes: List[TileAttribute]) -> None:
        """Set tile attributes."""
        for attr in attributes:
            self._attributes.set_attribute(attr)

    def unset_attribute(self, attribute: TileAttribute) -> None:
        """Unset a tile attribute."""
        self._attributes -= 1<<attribute

    def unset_attributes(self, *attributes: List[TileAttribute]) -> None:
        """Unset tile attributes."""
        for attr in attributes:
            self._attributes.unset_attribute(attr)

    def get_attributes(self) -> List[TileAttribute]:
        """Get a list of all tile attributes."""
        return [1<<x for x in bytearray(struct.pack("f", self._attributes)) if x == 1]

    def has_attribute(self, attribute: TileAttribute) -> bool:
        """Check if the tile has a certain attribute."""
        return self._attributes & (1 << attribute)
