import os
import math
import shutil
from typing import List
from random import randint
from argparse import ArgumentParser

from .constants import layers, BGT_DATA_PATH, GPKG_DATA_PATH, TIFF_DATA_PATH
from .classes import Grid, Point, Rect, TileData, TiffReader, TileAttribute, Visualizer
from .helpers import download_bgt_data, wkt_rect_from_corners


def parse_rdc(arg: List[str]):
    x, y = arg[0].split(",")
    return int(x), int(y)


def main():
    parser = ArgumentParser(
        prog="Pathfinder", description="Find a GEOJSON path in BGT data"
    )
    parser.add_argument(
        "--skip-bgt-download",
        help="Skip downloading BGT data and transforming to TIFF",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--resolution",
        help="Resolution of the grid",
        action="store",
        type=float,
        required=False,
        default=1.0,
    )
    parser.add_argument(
        "--padding",
        help="Add padding to the grid around the path's corners",
        action="store",
        type=float,
        required=False,
        default=0.1,
    )
    parser.add_argument(
        "start",
        help="RDC of the path start: x,y",
        nargs=1,
        action="store",
    )
    parser.add_argument(
        "end",
        help="RDC of the path end: x,y",
        nargs=1,
        action="store",
    )
    args = parser.parse_args()

    path_start = parse_rdc(args.start)
    path_end = parse_rdc(args.end)
    path_x_start, path_y_start = path_start
    path_x_end, path_y_end = path_end
    path_x_min = min(path_x_start, path_x_end)
    path_y_min = min(path_y_start, path_y_end)
    path_x_max = max(path_x_start, path_x_end)
    path_y_max = max(path_y_start, path_y_end)
    path_width = path_x_max - path_x_min
    path_height = path_y_max - path_y_min
    path_width_offset = int(args.padding * path_width)
    path_height_offset = int(args.padding * path_height)

    grid_x_min = path_x_min - path_width_offset
    grid_y_min = path_y_min - path_height_offset
    grid_x_max = path_x_max + path_width_offset + 1
    grid_y_max = path_y_max + path_height_offset + 1
    grid_width = grid_x_max - grid_x_min
    grid_height = grid_y_max - grid_y_min
    wkt_rect = wkt_rect_from_corners((grid_x_min, grid_y_min), (grid_x_max, grid_y_max))

    grid_zoomed_width = math.ceil(grid_width / args.resolution)
    grid_zoomed_height = math.ceil(grid_height / args.resolution)
    grid = Grid(Rect(grid_zoomed_width, grid_zoomed_height))

    if not args.skip_bgt_download:
        if os.path.isdir(BGT_DATA_PATH):
            shutil.rmtree(BGT_DATA_PATH)
        os.makedirs(BGT_DATA_PATH)
        if os.path.isdir(GPKG_DATA_PATH):
            shutil.rmtree(GPKG_DATA_PATH)
        os.makedirs(GPKG_DATA_PATH)
        if os.path.isdir(TIFF_DATA_PATH):
            shutil.rmtree(TIFF_DATA_PATH)
        os.makedirs(TIFF_DATA_PATH)

        print(f"Downloading BGT data for a {grid_width}x{grid_height} grid..")
        success, err = download_bgt_data(
            wkt_rect,
            [layer.layer_name for layer in layers],
        )
        if success:
            print("Download successful")
        else:
            print(f"Download failed: {err}")
            return

    print(
        f"\nRasterizing to TIFF files and loading into {grid_width}x{grid_height} grid.."
    )
    for layer in layers:
        TiffReader.read_tiffs(
            grid,
            layer,
            wkt_rect,
            args.resolution,
            input_dir=BGT_DATA_PATH,
            gpkg_dir=GPKG_DATA_PATH,
            output_dir=TIFF_DATA_PATH,
            outputBounds=(grid_x_min, grid_y_min, grid_x_max, grid_y_max),
        )
    c = 0
    for x in range(grid.dimensions.width):
        for y in range(grid.dimensions.height):
            if not grid.get_registered((x, y)):
                c += 1
                grid.register_tile_at((x, y), weight=10000)
    print(f"{c} unregistered tiles")

    print("\nFinding path..")
    path = grid.find_path(
        (
            int((path_x_start - path_x_min + path_width_offset) / args.resolution),
            int((path_y_start - path_y_min + path_height_offset) / args.resolution),
        ),
        (
            int((path_x_end - path_x_min + path_width_offset) / args.resolution),
            int((path_y_end - path_y_min + path_height_offset) / args.resolution),
        ),
    )

    print("\nTransforming path to GEOJSON..")
    Visualizer(
        [path], (grid_x_min, args.resolution, 0, grid_y_min, 0, args.resolution)
    ).getGEOJSON("path_1")


if __name__ == "__main__":
    main()
