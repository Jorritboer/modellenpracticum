from typing import List

from .tile_attribute import TileAttribute


class TileData:
    """Holds generic information on tiles."""

    _weight: float
    _attributes: set[TileAttribute]

    def __init__(self, **kwargs):
        """
        Optional arguments:
        weight: float -- base cost of the tile, default 0
        attributes: List[TileAttribute] -- attributes of the tile
        """
        self._weight = kwargs.get("weight") or 0
        self._attributes = set(kwargs.get("attributes") or [])

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
        self._attributes.add(attribute)

    def set_attributes(self, *attributes: List[TileAttribute]) -> None:
        """Set tile attributes."""
        self._attributes.update(attributes)

    def unset_attribute(self, attribute: TileAttribute) -> None:
        """Unset a tile attribute."""
        self._attributes.discard(attribute)

    def unset_attributes(self, *attributes: List[TileAttribute]) -> None:
        """Unset tile attributes."""
        self._attributes.difference_update(attributes)

    def get_attributes(self) -> List[TileAttribute]:
        """Get a list of all tile attributes."""
        return list(self._attributes)

    def has_attribute(self, attribute: TileAttribute) -> bool:
        """Check if the tile has a certain attribute."""
        return attribute in self._attributes
