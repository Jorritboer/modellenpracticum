import matplotlib.pyplot as plt
from random import randint
import json
import os
from typing import Tuple
from ..constants.paths import GEOJSON_DATA_PATH
from ..classes import Grid


class Visualizer:
    """Visualization purposes of found path"""

    # path: found path
    # geotransform: (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size)
    # grid. Necessary for smoothing
    def __init__(self, paths, grid: Grid, geotransform=(0, 0.5, 0, 0, 0, 0.5)) -> None:
        self.paths = [[(p[0], p[1]) for p in path] for path in paths]
        self.geotransform = geotransform
        self.grid = grid
        pass

    # adaptation of algorithm in https://www.gamedeveloper.com/programming/toward-more-realistic-pathfinding
    def smooth(self, path) -> list:
        path = path.copy()

        def path_through_same_cost(p1: Tuple[int, int], p2: Tuple[int, int]):
            return randint(0, 8) != 0

        checkPoint = 0
        currentPoint = 1
        while currentPoint + 1 < len(path):
            if path_through_same_cost(path[checkPoint], path[currentPoint + 1]):
                # make straight path between those points
                path.pop(currentPoint)
            else:
                checkPoint = currentPoint
                currentPoint += 1
        return path

    def array_index_to_coordinates(
        self,
        array_index_to_transform: list,
        geotransform: list,
    ) -> list:
        """
        Change index values of a raster (combined with geotransform) to real coordinates.
        Example: (306, 886) should become (174768.627, 451001.5161999986) given (174615.377, 451444.7661999986)

        Follow these steps:
        1. Use upper left coordinates
        2. add difference in x, but consider tile-size (default 0.5x0.5),
        3. Take the centre of the tile

        Note that in different coordinate systems, y_size can be negative (even though one might not expect it),
        there an abs() is used
        """
        (
            upper_left_x,
            x_size,
            x_rotation,
            upper_left_y,
            y_rotation,
            y_size,
            grid_height,
        ) = geotransform

        real_coordinates = []

        for x_index, y_index in array_index_to_transform:
            x = upper_left_x + (x_index * x_size) + (x_size / 2)

            y = upper_left_y + ((grid_height - y_index) * y_size) + (y_size / 2)

            real_coordinates.append((x, y))

        return real_coordinates

    def getGEOJSON(self, name: str = "path"):
        pathfeatures = [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        list(coord)
                        for coord in self.array_index_to_coordinates(
                            self.smooth(path), self.geotransform
                        )
                    ],
                },
                # style doesn't work
                # "style": {
                #     "fill": "blue",
                #     "stroke-width": "3",
                # },
            }
            for path in self.paths
            if path is not None
        ]

        dictionary = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:28992"}},
            "features": pathfeatures,
        }

        if not os.path.exists(GEOJSON_DATA_PATH):
            os.makedirs(GEOJSON_DATA_PATH)
        with open(os.path.join(GEOJSON_DATA_PATH, name + "_smooth.geojson"), "w") as f:
            json.dump(dictionary, f, indent=4)

        pathfeatures = [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        list(coord)
                        for coord in self.array_index_to_coordinates(
                            path, self.geotransform
                        )
                    ],
                },
                # style doesn't work
                # "style": {
                #     "fill": "blue",
                #     "stroke-width": "3",
                # },
            }
            for path in self.paths
            if path is not None
        ]

        dictionary = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:28992"}},
            "features": pathfeatures,
        }

        if not os.path.exists(GEOJSON_DATA_PATH):
            os.makedirs(GEOJSON_DATA_PATH)
        with open(os.path.join(GEOJSON_DATA_PATH, name + ".geojson"), "w") as f:
            json.dump(dictionary, f, indent=4)

    def show(self):
        for path in self.paths:
            colour = (randint(0, 255), randint(0, 255), randint(0, 255))
            plt.plot(
                [x[0] for x in path],
                [
                    x[1]
                    for x in self.array_index_to_coordinates(path, self.geotransform)
                ],
                linestyle="dotted",
                color=colour,
            )
        plt.show()
