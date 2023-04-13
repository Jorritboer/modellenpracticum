import subprocess
from osgeo import gdal, gdalconst
from typing import List, Optional, Tuple
import os

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
    input_filename: str, output_filename: str, column: str, value: str
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
            where=f"{column}='{value}'",
        ),
    )

    print(f"Created {output_filename}")
    return output_filename


class Layer:
    _gml_filename: str
    _layer_name: str
    _features: List[Tuple[str, str]]
    _linearized: Optional[str] = None
    _rasterized: Optional[List[str]] = None

    def __init__(
        self, gml_filename: str, layer_name: str, features: List[Tuple[str, str]]
    ):
        self._gml_filename = gml_filename
        self._layer_name = layer_name
        self._features = features

    def linearize(self, output_dir: Optional[str] = None) -> str:
        if self._linearized:
            return self._linearized

        output_filename = f"{self._layer_name}.gpkg"
        if output_dir:
            output_filename = f"{output_dir}/{output_filename}"

        if os.path.isfile(output_filename):
            self._linearized = output_filename
            return self._linearized

        self._linearized = linearize(self._gml_filename, output_filename)
        return self._linearized

    def rasterize(self, output_dir: Optional[str] = None) -> List[str]:
        if self._rasterized:
            return self._rasterized

        outputs = []
        for (column, value) in self._features:
            output_filename = f"{self._layer_name}-{value}.tiff"
            if output_dir:
                output_filename = f"{output_dir}/{output_filename}"

            output = rasterize(
                self.linearize(output_dir=output_dir),
                output_filename,
                column,
                value,
            )
            outputs += [output]

        return self._rasterized


layers = [
    Layer(
        gml_filename="extract2/bgt_wegdeel.gml",
        layer_name="wegdeel",
        features=[
            ("function", "voetpad"),
            ("function", "parkeervlak"),
            ("function", "spoorbaan"),
            ("function", "overweg"),
            ("function", "voetgangersgebied"),
            ("function", "voetpad"),
            ("function", "voetpad op trap"),
            ("function", "fietspad"),
            ("function", "rijbaan autoweg"),
            ("function", "rijbaan lokale weg"),
            ("function", "rijbaan regionale weg"),
            ("function", "baan voor vliegverkeer"),
            ("function", "rijbaan autosnelweg"),
            ("function", "inrit"),
            ("function", "woonerf"),
            ("function", "ruiterpad"),
            ("function", "ov baan"),
            ("surfaceMaterial", "open verharding"),
            ("surfaceMaterial", "half verhard"),
            ("surfaceMaterial", "onverhard"),
            ("surfaceMaterial", "gesloten verharding"),
        ],
    ),
    Layer(
        gml_filename="extract2/bgt_begroeidterreindeel.gml",
        layer_name="begroeidterreindeel",
        features=[
            ("class", "grasland overig"),
            ("class", "heide"),
            ("class", "moeras"),
            ("class", "grasland agrarisch"),
            ("class", "fruitteelt"),
            ("class", "boomteelt"),
            ("class", "kwelder"),
            ("class", "groenvoorziening"),
            ("class", "naaldbos"),
            ("class", "rietland"),
            ("class", "houtwal"),
            ("class", "bouwland"),
            ("class", "struiken"),
            ("class", "gemengd bos"),
            ("class", "loofbos"),
            ("class", "duin"),
        ],
    ),
]
for layer in layers:
    layer.rasterize(output_dir="output2")
