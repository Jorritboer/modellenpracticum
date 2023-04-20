import rasterio
from .grid import Grid
from .rect import Rect
from .tile_data import TileData


class TiffReader:
    """Import tiff files"""

    def read_tiff(src: str, grid: Grid, weight=1):
        print("reading tiff file")
        with rasterio.open(src) as tiff:
            array = tiff.read(1)
            for x in range(len(array)):
                for y in range(len(array[x])):
                    if array[x][y] > 0:
                        grid.register_tile_at((x, y), weight=weight)
        print("done reading tiff file")
        return grid
