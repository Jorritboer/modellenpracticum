import subprocess
from osgeo import gdal, gdalconst
from typing import Optional


def linearize(wkt_geometry: str, input_filename: str, output_filename: str):
    subprocess.run(
        [
            "ogr2ogr",
            "-nlt",
            "CONVERT_TO_LINEAR",
            "-skipfailures",
            "-clipdst",
            wkt_geometry,
            output_filename,
            input_filename,
        ],
        check=True,
    )
    return output_filename


def rasterize(
    input_filename: str,
    output_filename: str,
    where: Optional[str] = None,
    resolution: float = 1.0,  # in meters
) -> str:
    gdal.Rasterize(
        output_filename,
        input_filename,
        options=gdal.RasterizeOptions(
            burnValues=[255],
            allTouched=True,
            creationOptions=["COMPRESS=LZW", "TILED=YES"],
            outputType=gdalconst.GDT_Byte,
            xRes=resolution,
            yRes=resolution,
            where=where,
        ),
    )
    return output_filename
