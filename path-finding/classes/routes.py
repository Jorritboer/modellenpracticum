from .grid import Grid
from .rect import Rect
from .point import Point
from .tile_data import TileData

from random import randint
from math import inf


def main(no_routes: int = 2, radius: int = 3, multiplier: int = 10) -> None:
    grid = Grid(Rect(100, 100))
    for i in range(100):
        for j in range(100):
            grid.register_tile_at(
                Point(i, j), TileData(weight=500 if i == j else randint(0, 50))
            )
    first_path = grid.find_path(Point(0, 0), Point(99, 99))
    second_path = grid.find_path(
        Point(0, 0),
        Point(99, 99),
        existing_paths=[first_path],
        existing_path_multiplier=69,
        existing_path_radius=5,
    )
    print(grid.path_to_string(second_path))


main()
