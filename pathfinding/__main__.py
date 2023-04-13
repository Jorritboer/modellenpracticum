from random import randint

from .classes import Grid, Rect, TileAttribute
from .classes.visualizer import Visualizer


def main():
    # Test 1
    print("Simple 5x5 path")

    grid = Grid(Rect(5, 5))
    grid.register_tile_at((0, 0))
    grid.register_tile_at((1, 0), weight=2)
    grid.register_tile_at((2, 0), weight=2)
    grid.register_tile_at((3, 0), weight=2)
    grid.register_tile_at((4, 0), weight=2)
    grid.register_tile_at((4, 1), weight=2)
    grid.register_tile_at((4, 2), weight=2)
    grid.register_tile_at((4, 3), weight=2, attributes=[TileAttribute.Road])
    grid.register_tile_at((4, 4), weight=2)

    grid.register_tile_at((2, 1), weight=1)
    grid.register_tile_at((2, 2), weight=1)
    grid.register_tile_at((2, 3), weight=1)
    grid.register_tile_at((1, 3), weight=1)

    print(
        grid.path_to_string(grid.find_path((0, 0), (4, 4), path_cost=1, max_length=9))
    )

    # Test 2
    print("\nSimple 5x5 path with attributes")

    grid = Grid(Rect(5, 5))
    grid.register_tile_at((0, 0))
    grid.register_tile_at((1, 0), weight=1, attributes=[TileAttribute.Road])
    grid.register_tile_at((2, 0), weight=1, attributes=[TileAttribute.Road])
    grid.register_tile_at((3, 0), weight=1, attributes=[TileAttribute.Road])
    grid.register_tile_at((4, 0), weight=1, attributes=[TileAttribute.Road])
    grid.register_tile_at((4, 1), weight=1, attributes=[TileAttribute.Road])
    grid.register_tile_at((4, 2), weight=1, attributes=[TileAttribute.Road])
    grid.register_tile_at((4, 3), weight=1, attributes=[TileAttribute.Road])
    grid.register_tile_at((4, 4), weight=1)
    grid.register_tile_at((1, 1), weight=1, attributes=[TileAttribute.Water])
    grid.register_tile_at((2, 2), weight=1, attributes=[TileAttribute.Water])
    grid.register_tile_at((3, 3), weight=1, attributes=[TileAttribute.Water])

    print(
        grid.path_to_string(
            grid.find_path(
                (0, 0),
                (4, 4),
                path_cost=1,
                max_length=9,
                attribute_multipliers={
                    TileAttribute.Road: 0.5,
                    TileAttribute.Water: 10,
                },
            )
        )
    )

    # Test 3
    print("\nRandom 100x100 path, discouraging diagonal")

    grid = Grid(Rect(100, 100))
    for i in range(100):
        for j in range(100):
            grid.register_tile_at((i, j), weight=500 if i == j else randint(0, 50))
    first_path = grid.find_path((0, 0), (99, 99))
    print(grid.path_to_string(first_path))

    # Test 4
    print("\nRandom 100x100 path, discouraging diagonal with previous path")
    print(
        grid.path_to_string(
            grid.find_path(
                (0, 0),
                (99, 99),
                existing_paths=[first_path],
                existing_path_multiplier=69,
                existing_path_radius=5,
            )
        )
    )

    # Test 5
    print("\nRandom 256x256 path, discouraging diagonal with previous path")
    grid = Grid(Rect(256, 256))
    for i in range(256):
        for j in range(256):
            grid.register_tile_at(
                (i, j), weight=500 if i == j else randint(0, 50)
            )
    first_path = grid.find_path((0, 0), (255, 255))
    print(grid.path_to_string([first_path]))

    # Test 6
    print("\nRandom 512x512 path, discouraging diagonal with previous path")
    grid = Grid(Rect(512, 512))
    for i in range(512):
        for j in range(512):
            grid.register_tile_at(
                (i, j), weight=500 if i == j else randint(0, 50)
            )
    first_path = grid.find_path((0, 0), (511, 511))
    l = []
    print(grid.path_to_string(first_path))

    visualizer = Visualizer([first_path])
    visualizer.getGEOJSON()
    
    # Test 7
    print("\nRandom 1024x1024 path, discouraging diagonal with previous path")
    grid = Grid(Rect(1024, 1024))
    for i in range(1024):
        for j in range(1024):
            grid.register_tile_at(
                (i, j), weight=500 if i == j else randint(0, 50)
            )
    first_path = grid.find_path((0, 0), (1023, 1023))
    print(grid.path_to_string(first_path))
    


if __name__ == "__main__":
    main()
