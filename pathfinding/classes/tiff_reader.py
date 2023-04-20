import rasterio
import os
from typing import Tuple

from typing import Optional
from .layer import Layer
from .tile_attribute import TileAttribute
from .grid import Grid
from .rect import Rect
from .tile_data import TileData


class TiffReader:
    """Import tiff files"""

    def _read_tiff(grid: Grid, src: str, attribute: TileAttribute, weight=1):
        if not os.path.exists(src):
            print(f"warning: skipping tiff {src}")
            return grid

        print(f"reading tiff file {src}")
        with rasterio.open(src) as tiff:
            array = tiff.read(1)
            for y in range(len(array)):
                for x in range(len(array[y])):
                    if array[y][x] > 0:
                        grid.register_tile_at(
                            (x, y), weight=weight, attributes=[attribute]
                        )
        print("done reading tiff file")
        return grid

    def read_tiffs(
        grid: Grid,
        layer: Layer,
        wkt_geometry: str,
        resolution: float,
        input_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        outputBounds: Optional[Tuple[float, float, float, float]] = None,
    ):
        tiffs = layer.rasterize(
            wkt_geometry,
            resolution=resolution,
            input_dir=input_dir,
            gpkg_dir=output_dir,
            output_dir=output_dir,
            outputBounds=outputBounds,
        )
        for tiff, feature in tiffs:
            TiffReader._read_tiff(grid, tiff, feature.attribute)
