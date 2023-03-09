class TileData:
    """Holds generic information on tiles."""

    _weight: float

    def __init__(self, **kwargs):
        """
        Optional arguments:
        weight: float -- base cost of the tile, default 0
        """
        self._weight = kwargs.get("weight") or 0

    @property
    def weight(self) -> float:
        """Get the tile's base cost."""
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        """Set the tile's base cost."""
        self._weight = value