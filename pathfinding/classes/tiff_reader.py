import rasterio

from typing import Optional
from rasterize.layer import Layer
from .tile_attribute import TileAttribute
from .grid import Grid
from .rect import Rect
from .tile_data import TileData


class TiffReader:
    """Import tiff files"""

    def _read_tiff(grid: Grid, src: str, attribute: TileAttribute, weight=1):
        print("reading tiff file")
        with rasterio.open(src) as tiff:
            array = tiff.read(1)
            for x in range(len(array)):
                for y in range(len(array[x])):
                    if array[x][y] > 0:
                        grid.register_tile_at(
                            (x, y), weight=weight, attributes=[attribute]
                        )
        print("done reading tiff file")
        return grid

    def read_tiffs(
        grid: Grid,
        layer: Layer,
        input_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
    ):
        tiffs = layer.rasterize(input_dir=input_dir, output_dir=output_dir)
        for tiff, feature in tiffs:
            TiffReader._read_tiff(grid, tiff, feature.attribute)
