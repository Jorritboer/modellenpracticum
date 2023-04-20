import subprocess
import os
from osgeo import gdal, gdalconst
from typing import Optional, List, Tuple

RESOLUTION = 1.0  # meter


def linearize(input_filename: str, output_filename: str):
    print(f"Linearizing {input_filename} to {output_filename}...")

    subprocess.run(
        [
            "ogr2ogr",
            "-nlt",
            "CONVERT_TO_LINEAR",
            "-skipfailures",
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
) -> str:
    print(f"Rasterizing {input_filename} to {output_filename}...")

    gdal.Rasterize(
        output_filename,
        input_filename,
        options=gdal.RasterizeOptions(
            burnValues=[255],
            allTouched=True,
            creationOptions=["COMPRESS=LZW", "TILED=YES"],
            outputType=gdalconst.GDT_Byte,
            xRes=RESOLUTION,
            yRes=RESOLUTION,
            where=where,
        ),
    )

    print(f"Created {output_filename}")
    return output_filename


class Layer:
    _gml_filename: str
    _layer_name: str
    _features: List[Tuple[Optional[str], int]]
    _linearized: Optional[str] = None
    _rasterized: Optional[List[str]] = None

    def __init__(
        self,
        gml_filename: str,
        layer_name: str,
        features: List[Tuple[Optional[str], int]],
    ):
        self._gml_filename = gml_filename
        self._layer_name = layer_name  # table name
        self._features = features
        # feature is a tuple of where clause and value

    def linearize(
        self, input_dir: Optional[str] = None, output_dir: Optional[str] = None
    ) -> str:
        if self._linearized:
            return self._linearized

        input_filename = self._gml_filename
        if input_dir:
            input_filename = f"{input_dir}/{input_filename}"

        output_filename = f"{self._layer_name}.gpkg"
        if output_dir:
            output_filename = f"{output_dir}/{output_filename}"

        if os.path.isfile(output_filename):
            self._linearized = output_filename
            return self._linearized

        self._linearized = linearize(input_filename, output_filename)
        return self._linearized

    def rasterize(
        self, input_dir: Optional[str] = None, output_dir: Optional[str] = None
    ) -> List[str]:
        if self._rasterized:
            return self._rasterized

        outputs = []
        for feature_name, where, _ in self._features:
            output_filename = f"{self._layer_name}_{feature_name}.tiff"
            if output_dir:
                output_filename = f"{output_dir}/{output_filename}"

            output = rasterize(
                self.linearize(input_dir=input_dir, output_dir=output_dir),
                output_filename,
                where=where,
            )
            outputs += [output]

        return self._rasterized