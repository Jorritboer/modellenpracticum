import os
from typing import Optional, List, Tuple

from .tile_attribute import TileAttribute
from ..helpers.transformations import linearize, rasterize


class Feature:
    name: str
    where: Optional[str]
    attribute: TileAttribute
    weight: int

    def __init__(
        self,
        name: str,
        where: Optional[str],
        attribute: TileAttribute,
        weight: int,
    ):
        self.name = name
        self.where = where
        self.attribute = attribute
        self.weight = weight


class Layer:
    _gml_filename: str
    _layer_name: str
    _features: List[Feature]
    _linearized: Optional[str] = None
    _rasterized: Optional[List[Tuple[str, Feature]]] = None

    def __init__(
        self,
        gml_filename: str,
        layer_name: str,
        features: List[Feature],
    ):
        self._gml_filename = gml_filename
        self._layer_name = layer_name  # table name
        self._features = features
        # feature is a tuple of where clause and value

    @property
    def layer_name(self) -> str:
        return self._layer_name

    def linearize(
        self,
        wkt_geometry: str,
        input_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> str:
        if self._linearized:
            return self._linearized

        input_filename = self._gml_filename
        if input_dir:
            input_filename = f"{input_dir}/{input_filename}"

        output_filename = f"{self._layer_name}.gpkg"
        if output_dir:
            output_filename = f"{output_dir}/{output_filename}"

        # if os.path.isfile(output_filename):
        #     self._linearized = output_filename
        #     return self._linearized

        self._linearized = linearize(wkt_geometry, input_filename, output_filename)
        return self._linearized

    def rasterize(
        self,
        wkt_geometry: str,
        resolution: float,
        input_dir: Optional[str] = None,
        gpkg_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        outputBounds: Optional[Tuple[float, float, float, float]] = None,
    ) -> List[Tuple[str, Feature]]:
        if self._rasterized:
            return self._rasterized

        outputs = []
        for feature in self._features:
            output_filename = f"{self._layer_name}_{feature.name}.tiff"
            if output_dir:
                output_filename = f"{output_dir}/{output_filename}"

            output = rasterize(
                self.linearize(wkt_geometry, input_dir=input_dir, output_dir=gpkg_dir),
                output_filename,
                where=feature.where,
                resolution=resolution,
                outputBounds=outputBounds,
            )
            outputs += [(output, feature)]

        self._rasterized = outputs
        return self._rasterized
