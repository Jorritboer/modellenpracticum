from random import randint

from .classes import Grid, Point, Rect, TileData, TiffReader, TileAttribute
from .helpers import download_bgt_data, wkt_rect_from_corners
from .classes.visualizer import Visualizer
from rasterize.weights import layers


def main():
    print("creating grid")
    grid = Grid(Rect(4000, 4000))
    print("grid created")
    for layer in layers:
        TiffReader.read_tiffs(grid, layer, input_dir="extract", output_dir="output")

    print(grid.find_path((0, 0), (10, 10)))


if __name__ == "__main__":
    main()
