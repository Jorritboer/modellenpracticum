import os
import shutil
from random import randint

from .constants import layers, BGT_DATA_PATH, GPKG_DATA_PATH, TIFF_DATA_PATH
from .classes import Grid, Point, Rect, TileData, TiffReader, TileAttribute, Visualizer
from .helpers import download_bgt_data, wkt_rect_from_corners


def main():
    print("Downloading BGT data..")
    wkt_rect = wkt_rect_from_corners((140100, 200000), (151000, 250000))
    success, err = download_bgt_data(
        wkt_rect,
        [layer.layer_name for layer in layers],
    )
    if success:
        print("Download successful")
    else:
        print(f"Download failed: {err}")
        return

    print("\nLinearizing and rasterizing downloaded gml files..")
    if os.path.isdir(GPKG_DATA_PATH):
        shutil.rmtree(GPKG_DATA_PATH)
    os.mkdir(GPKG_DATA_PATH)
    if os.path.isdir(TIFF_DATA_PATH):
        shutil.rmtree(TIFF_DATA_PATH)
    os.mkdir(TIFF_DATA_PATH)
    for layer in layers:
        layer.rasterize(wkt_rect, BGT_DATA_PATH, GPKG_DATA_PATH, TIFF_DATA_PATH)

    # print("creating grid")
    # grid = Grid(Rect(2000, 2000))
    # print("grid created")
    # TiffReader.read_tiff("testdata/begroeidterreindeel.tiff", grid, 1)
    # TiffReader.read_tiff("testdata/onbegroeidterreindeel.tiff", grid, 500)
    # c = 0
    # for x in range(grid.dimensions.width):
    #    for y in range(grid.dimensions.height):
    #        if not grid.get_registered((x, y)):
    #            c += 1
    #            grid.register_tile_at((x, y), weight=1000)
    # print(grid.find_path((0, 0), (1999, 1999)))


if __name__ == "__main__":
    main()
