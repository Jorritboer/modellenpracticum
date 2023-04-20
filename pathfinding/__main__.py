import os
import shutil
from random import randint

from .constants import layers, BGT_DATA_PATH, GPKG_DATA_PATH, TIFF_DATA_PATH
from .classes import Grid, Point, Rect, TileData, TiffReader, TileAttribute, Visualizer
from .helpers import download_bgt_data, wkt_rect_from_corners

rdc_ah = (188598, 427829)
rdc_left_bottom = (188359, 427562)
rdc_right_bottom = (188840, 427045)
rdc_right_top = (188808, 428168)
rdc_left_top = (188361, 428175)
RESOLUTION = 0.5


def main():
    print("Downloading BGT data...")
    bounds = (rdc_ah, rdc_left_bottom)
    x_min = 188359
    y_min = 427562
    x_max = 188598
    y_max = 427829
    wkt_rect = wkt_rect_from_corners(*bounds)
    success, err = download_bgt_data(
        wkt_rect,
        [layer.layer_name for layer in layers],
    )
    if success:
        print("Download successful")
    else:
        print(f"Download failed: {err}")
        return

    # print("\nLinearizing and rasterizing downloaded gml files..")
    # if os.path.isdir(GPKG_DATA_PATH):
    #     shutil.rmtree(GPKG_DATA_PATH)
    # os.mkdir(GPKG_DATA_PATH)
    # if os.path.isdir(TIFF_DATA_PATH):
    #     shutil.rmtree(TIFF_DATA_PATH)
    # os.mkdir(TIFF_DATA_PATH)
    # for layer in layers:
    #     layer.rasterize(wkt_rect, BGT_DATA_PATH, GPKG_DATA_PATH, TIFF_DATA_PATH)

    grid = Grid(Rect(478 + 1, 534 + 1))
    for layer in layers:
        TiffReader.read_tiffs(
            grid,
            layer,
            wkt_rect,
            input_dir=".bgt_data",
            output_dir="output",
            outputBounds=(x_min, y_min, x_max, y_max),
            resolution=RESOLUTION,
        )

    # print("creating grid")
    # print("grid created")
    # TiffReader.read_tiff("testdata/begroeidterreindeel.tiff", grid, 1)
    # TiffReader.read_tiff("testdata/onbegroeidterreindeel.tiff", grid, 500)
    # print(grid.find_path((0, 0), (1999, 1999)))
    c = 0
    for x in range(grid.dimensions.width):
        for y in range(grid.dimensions.height):
            if not grid.get_registered((x, y)):
                c += 1
                grid.register_tile_at((x, y), weight=1000)
    print(f"{c} unregistered tiles")
    # path = grid.find_path((0, 0), (478 // 2, 534 // 2))
    path = grid.find_path((0, 534), (478, 0))
    Visualizer([path], (x_min, RESOLUTION, 0, y_min, 0, RESOLUTION)).getGEOJSON(
        "output.geojson"
    )


if __name__ == "__main__":
    main()
