import subprocess
from osgeo import gdal, gdalconst
import argparse
import os

RESOLUTION = 1.0  # meter


def rasterize(extract: str, output: str, layer: str):
    gml_filename = f"{extract}/{layer}.gml"
    gml_ogr2ogr_filename = f"{output}/{layer}_ogr2ogr.gml"
    tiff_filename = f"{output}/{layer}.tiff"

    print(f"Converting {gml_filename} to {gml_ogr2ogr_filename}...")

    subprocess.run(
        ["ogr2ogr", "-nlt", "CONVERT_TO_LINEAR", gml_ogr2ogr_filename, gml_filename],
        check=True,
    )

    print(f"Rasterizing {gml_ogr2ogr_filename} to {tiff_filename}...")

    gdal.Rasterize(
        tiff_filename,
        gml_ogr2ogr_filename,
        options=gdal.RasterizeOptions(
            burnValues=[255],
            allTouched=True,
            creationOptions=["COMPRESS=LZW", "TILED=YES"],
            outputType=gdalconst.GDT_Byte,
            xRes=RESOLUTION,
            yRes=RESOLUTION,
        ),
    )

    print(f"Created {tiff_filename}")


layers = [
    "bgt_bak",
    "bgt_begroeidterreindeel",
    "bgt_bord",
    "bgt_functioneelgebied",
    "bgt_gebouwinstallatie",
    "bgt_installatie",
    "bgt_kast",
    "bgt_kunstwerkdeel",
    "bgt_mast",
    "bgt_onbegroeidterreindeel",
    "bgt_ondersteunendwaterdeel",
    "bgt_ondersteunendwegdeel",
    "bgt_ongeclassificeerdobject",
    "bgt_openbareruimtelabel",
    "bgt_overbruggingsdeel",
    "bgt_overigbouwwerk",
    "bgt_overigescheiding",
    "bgt_paal",
    "bgt_pand",
    "bgt_put",
    "bgt_scheiding",
    "bgt_sensor",
    "bgt_spoor",
    "bgt_straatmeubilair",
    "bgt_tunneldeel",
    "bgt_vegetatieobject",
    "bgt_waterdeel",
    "bgt_waterinrichtingselement",
    "bgt_wegdeel",
    "bgt_weginrichtingselement",
]

parser = argparse.ArgumentParser(
    prog="rasterize.py", description="Rasterize BGT GML files"
)
parser.add_argument("extract", help="Path to unzipped BGT extract")
parser.add_argument("output", help="Path to output directory")
args = parser.parse_args()

try:
    os.mkdir(args.output)
except FileExistsError:
    pass

for layer in layers:
    rasterize(args.extract, args.output, layer)
