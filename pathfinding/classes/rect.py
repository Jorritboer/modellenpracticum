class Rect:
    """Describes a rectangular shape."""

    _width: float
    _height: float

    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        """Get the width of the rectangle."""
        return self._width

    @property
    def height(self) -> float:
        """Get the height of the rectangle."""
        return self._height

    def __str__(self):
        return str((self.width, self.height))

    def __eq__(self, other):
        return self._width == other._width and self._height == other._height

    def __ne__(self, other):
        return self._width != other._width or self._height != other._height
