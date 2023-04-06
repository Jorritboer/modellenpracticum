from random import randint

from .classes import Grid, Point, Rect, TileData, TiffReader


def main():
    print("creating grid")
    grid = Grid(Rect(2000, 2000))
    print("grid created")
    TiffReader.read_tiff("testdata/begroeidterreindeel.tiff", grid, 1)
    TiffReader.read_tiff("testdata/onbegroeidterreindeel.tiff", grid, 500)
    c = 0
    for x in range(grid.dimensions.width):
        for y in range(grid.dimensions.height):
            if not grid.get_registered((x, y)):
                c += 1
                grid.register_tile_at((x, y), weight=1000)
    print(grid.find_path((0, 0), (1999, 1999)))


if __name__ == "__main__":
    main()
