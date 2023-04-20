import matplotlib.pyplot as plt
from random import randint
import json
import os
from ..constants.paths import BGT_DATA_PATH


class Visualizer:
    """Visualization purposes of found path"""

    # path: found path
    # geotransform: (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size)
    def __init__(self, paths, geotransform=(0, 0.5, 0, 0, 0, 0.5)) -> None:
        self.paths = [[(p[0], p[1]) for p in path] for path in paths]
        self.geotransform = geotransform
        pass

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
        ) = geotransform

        real_coordinates = []

        for y_index, x_index in array_index_to_transform:
            x = upper_left_x + ((x_index * x_size) + (x_size / 2))

            y = upper_left_y - abs(((y_index * y_size) + (y_size / 2)))

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
                            path, self.geotransform
                        )
                    ],
                },
            }
            for path in self.paths
            if path is not None
        ]

        dictionary = {"type": "FeatureCollection", "features": pathfeatures}

        if not os.path.exists(BGT_DATA_PATH):
            os.makedirs(BGT_DATA_PATH)
        with open(os.path.join(BGT_DATA_PATH, name + ".json"), "a") as f:
            json.dump(dictionary, f, indent=0)

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
