from random import randint

from .classes import Grid, Point, Rect, TileData
from .classes.visualizer import Visualizer

def main():
    # Test 1
    print("Simple 5x5 path")

    grid = Grid(Rect(5, 5))
    grid.register_tile_at(Point(0, 0), TileData())
    grid.register_tile_at(Point(1, 0), TileData(weight=2))
    grid.register_tile_at(Point(2, 0), TileData(weight=2))
    grid.register_tile_at(Point(3, 0), TileData(weight=2))
    grid.register_tile_at(Point(4, 0), TileData(weight=2))
    grid.register_tile_at(Point(4, 1), TileData(weight=2))
    grid.register_tile_at(Point(4, 2), TileData(weight=2))
    grid.register_tile_at(Point(4, 3), TileData(weight=2))
    grid.register_tile_at(Point(4, 4), TileData(weight=2))

    grid.register_tile_at(Point(2, 1), TileData(weight=1))
    grid.register_tile_at(Point(2, 2), TileData(weight=1))
    grid.register_tile_at(Point(2, 3), TileData(weight=1))
    grid.register_tile_at(Point(1, 3), TileData(weight=1))

    print(
        grid.path_to_string(
            grid.find_path(Point(0, 0), Point(4, 4), path_cost=1, max_length=9)
        )
    )

    # Test 2
    print("\nRandom 100x100 path, discouraging diagonal")

    grid = Grid(Rect(100, 100))
    for i in range(100):
        for j in range(100):
            grid.register_tile_at(
                Point(i, j), TileData(weight=5000 if i == j else randint(0, 50))
            )
    first_path = grid.find_path(Point(0, 0), Point(99, 99))
    print(grid.path_to_string(first_path))
    print(first_path)
    # Test 3
    print("\nRandom 100x100 path, discouraging diagonal with previous path")
    second_path = grid.find_path(
                Point(0, 0),
                Point(99, 99),
                existing_paths=[first_path],
                existing_path_multiplier=600,
                existing_path_radius=2,
            )
    print(
        grid.path_to_string(second_path)
    )
    visualizer1 = Visualizer(first_path, (10, 0.5, 0, 10, 0, 0.5))
    visualizer2 = Visualizer(second_path, (10, 0.5, 0, 10, 0, 0.5))
    visualizer1.show()

if __name__ == "__main__":
    main()
