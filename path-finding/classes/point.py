from math import sqrt


class Point:
    """Describes a two-dimensional point."""

    _x: float
    _y: float

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        pass

    @property
    def x(self) -> float:
        """Get the x-coordinate of the point."""
        return self._x

    @property
    def y(self) -> float:
        """Get the y-coordinate of the point."""
        return self._y

    def dist(self, other: "Point") -> float:
        """Get the euclidian distance to another point."""
        return sqrt(self.dist_sq(other))

    def dist_sq(self, other: "Point") -> float:
        """
        Get the euclidian distance squared to another point.

        More efficient than dist, since we don't need to square root.
        """
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(f"Point({self.x},{self.y})")

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __ne__(self, other):
        return self._x != other._x or self._y != other._y
