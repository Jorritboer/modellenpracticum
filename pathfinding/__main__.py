import json
import os
import math
import shutil
from jsonschema import validate
from typing import List, Tuple
from random import randint
from argparse import ArgumentParser, Namespace

from .constants import (
    layers,
    layers_dict,
    BGT_DATA_PATH,
    CONFIG_DATA_PATH,
    GPKG_DATA_PATH,
    TIFF_DATA_PATH,
)
from .classes import Grid, Point, Rect, TileData, TiffReader, TileAttribute, Visualizer
from .helpers import download_bgt_data, wkt_rect_from_corners


def parse_rdc(arg: List[str]) -> Tuple[int, int]:
    """Parse RDC, i.e. a tuple of integers."""

    x, y = arg[0].split(",")
    return int(x), int(y)


def get_args() -> Namespace:
    """Get the args from argparser and parse options that need post-processing."""

    parser = ArgumentParser(
        prog="Pathfinder", description="Find a GEOJSON path in BGT data"
    )

    parser.add_argument(
        "--clear-cache",
        help="Remove all files from the cache",
        action="store_true",
    )
    parser.add_argument(
        "-m",
        "--existing-path-multiplier",
        help="How much more existing paths should be weighted when finding other paths",
        action="store",
        type=float,
        required=False,
        default=1.0,
    )
    parser.add_argument(
        "-r",
        "--existing-path-radius",
        help="Amount of meters of influence existing paths have",
        action="store",
        type=float,
        required=False,
        default=0.0,
    )
    parser.add_argument(
        "-f",
        "--fraction",
        help="if paths is equal to 2, find a different path for every [n*fraction: (n+1)*fraction] of the first path",
        action="store",
        type=float,
        required=False,
        default=1.0,
    )
    parser.add_argument(
        "-l",
        "--max-length",
        help="Maximum length of the path, in meters",
        action="store",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-o",
        "--output-name",
        help="Name of the output file",
        action="store",
        required=False,
        default="path",
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
        "-c",
        "--path-cost",
        help="Cost of the path per meter of length",
        action="store",
        type=float,
        required=False,
        default=0.0,
    )
    parser.add_argument(
        "-p",
        "--paths",
        help="Amount of paths to find, path 1 being the shortest",
        action="store",
        type=int,
        required=False,
        default=1,
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

    try:
        args.start = parse_rdc(args.start)
    except:
        print("Invalid start RDC")
        exit
    try:
        args.end = parse_rdc(args.end)
    except:
        print("Invalid start RDC")
        exit

    return args


def get_config() -> object:
    """
    Get the config, based on the one at CONFIG_DATA_PATH.

    Returns:
    {
        "attribute_weights": { [TileAttribute]?: number },
        "unregistered_weight": number
    }
    """

    try:
        file = open(CONFIG_DATA_PATH, "r")
        config = json.load(file)
    except FileNotFoundError:
        file = open(CONFIG_DATA_PATH, "w")
        config = {
            "layer_weights": {
                layer.layer_name: {
                    feature.name: feature.weight for feature in layer.features
                }
                for layer in layers
            },
            "unregistered_weight": 10000.0,
        }
        json.dump(config, file, indent=4)
    file.close()

    layer_weights = {
        layer.layer_name: {
            "type": "object",
            "properties": {
                feature.name: {"type": "number"} for feature in layer.features
            },
        }
        for layer in layers
    }
    schema = {
        "type": "object",
        "properties": {
            "layer_weights": {"type": "object", "properties": layer_weights},
            "unregistered_weight": {"type": "number"},
        },
        "additionalProperties": False,
        "minProperties": 2,
    }
    validate(instance=config, schema=schema)

    return {
        "attribute_weights": {
            layers_dict[layer_name].features_dict[feature_name].attribute: weight
            for layer_name, features in config["layer_weights"].items()
            for feature_name, weight in features.items()
        },
        "unregistered_weight": config["unregistered_weight"],
    }


def clear_cache():
    shutil.rmtree(BGT_DATA_PATH)
    shutil.rmtree(GPKG_DATA_PATH)
    shutil.rmtree(TIFF_DATA_PATH)


def main():
    args = get_args()
    config = get_config()

    if args.clear_cache:
        clear_cache()

    path_x_start, path_y_start = args.start
    path_x_end, path_y_end = args.end
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

    print(f"Downloading BGT data for a {grid_width}x{grid_height}m grid..")
    success, reason = download_bgt_data(
        wkt_rect,
        [layer.layer_name for layer in layers],
    )
    if success:
        if reason:
            print(f"Download successful: {reason}")
        else:
            print("Download successful")
    else:
        print(f"Download failed: {reason}")
        return

    print(
        f"\nRasterizing to TIFF files and loading into {grid_width}x{grid_height}m grid.."
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
                grid.register_tile_at((x, y), base_weight=config["unregistered_weight"])
    print(f"{c} unregistered tiles")

    existing_paths = []
    for i in range(args.paths):
        if i==1 and args.paths ==2 and not (args.fraction is None or  args.fraction >=1 or args.fraction <=0):
            
            intervals = [(args.fraction*n, args.fraction*(n+1)) for n in range(math.ceil(1/args.fraction)) if args.fraction*(n+1) <=1]
            print(intervals)
            for interval in intervals:
                print(f"\nFinding path_2[{interval[0]},{interval[1]}]")
                path = grid.find_path(
                (
                    int(
                        (
                            path_width_offset
                            if path_x_start < path_x_end
                            else (grid_width - path_width_offset)
                        )
                        / args.resolution
                    ),
                    int(
                        (
                            path_height_offset
                            if path_y_start > path_y_end
                            else (grid_height - path_height_offset)
                        )
                        / args.resolution
                    ),
                ),
                (
                    int(
                        (
                            (grid_width - path_width_offset)
                            if path_x_start < path_x_end
                            else path_width_offset
                        )
                        / args.resolution
                    ),
                    int(
                        (
                            (grid_height - path_height_offset)
                            if path_y_start > path_y_end
                            else path_height_offset
                        )
                        / args.resolution
                    ),
                ),
                max_length=None
                if args.max_length is None
                else args.max_length / args.resolution,
                path_cost=args.path_cost * args.resolution,
                existing_paths=[x[math.floor(interval[0]*len(x)): math.ceil(interval[1]*len(x))] for x in existing_paths],
                existing_path_multiplier=args.existing_path_multiplier,
                existing_path_radius=int(args.existing_path_radius / args.resolution),
                attribute_weights=config["attribute_weights"],
                
            )
                print("Transforming path to GEOJSON..")
                name = args.output_name 
                name += f"_2[{interval[0]},{interval[1]}]"
                Visualizer(
                    [path],
                    (
                        grid_x_min,
                        args.resolution,
                        0,
                        grid_y_min,
                        0,
                        args.resolution,
                        grid_zoomed_height,
                    ),
                ).getGEOJSON(name)
        else:
            print(f"\nFinding path {i+1}..")
            path = grid.find_path(
                (
                    int(
                        (
                            path_width_offset
                            if path_x_start < path_x_end
                            else (grid_width - path_width_offset)
                        )
                        / args.resolution
                    ),
                    int(
                        (
                            path_height_offset
                            if path_y_start > path_y_end
                            else (grid_height - path_height_offset)
                        )
                        / args.resolution
                    ),
                ),
                (
                    int(
                        (
                            (grid_width - path_width_offset)
                            if path_x_start < path_x_end
                            else path_width_offset
                        )
                        / args.resolution
                    ),
                    int(
                        (
                            (grid_height - path_height_offset)
                            if path_y_start > path_y_end
                            else path_height_offset
                        )
                        / args.resolution
                    ),
                ),
                max_length=None
                if args.max_length is None
                else args.max_length / args.resolution,
                path_cost=args.path_cost * args.resolution,
                existing_paths=existing_paths,
                existing_path_multiplier=args.existing_path_multiplier,
                existing_path_radius=int(args.existing_path_radius / args.resolution),
                attribute_weights=config["attribute_weights"],
            )
            existing_paths.append(path)

            print("Transforming path to GEOJSON..")
            name = args.output_name
            if args.paths > 1: 
                name += f"_{i+1}"
            Visualizer(
                [path],
                (
                    grid_x_min,
                    args.resolution,
                    0,
                    grid_y_min,
                    0,
                    args.resolution,
                    grid_zoomed_height,
                ),
            ).getGEOJSON(name)


if __name__ == "__main__":
    main()
