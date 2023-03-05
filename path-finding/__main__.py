from .classes import Grid, Point, Rect, TileData


def main():
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

    print(grid.find_path(Point(0, 0), Point(4, 4), path_cost=1, max_length=9))


if __name__ == "__main__":
    main()
