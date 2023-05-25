import os
from typing import Dict, Optional, List, Tuple

from .tile_attribute import TileAttribute
from ..helpers.hash import bgt_hash, gpkg_hash, tiff_hash
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

    @property
    def features(self) -> List[Feature]:
        return self._features

    @property
    def features_dict(self) -> Dict[str, Feature]:
        return {feature.name: feature for feature in self._features}

    def linearize(
        self,
        wkt_geometry: str,
        input_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> str:
        if self._linearized:
            return self._linearized

        bgt_prefix = bgt_hash(wkt_geometry)
        gpkg_prefix = gpkg_hash(wkt_geometry)

        input_filename = f"{bgt_prefix}_{self._gml_filename}"
        if input_dir:
            input_filename = os.path.join(input_dir, input_filename)

        output_filename = f"{gpkg_prefix}_{self._layer_name}.gpkg"
        if output_dir:
            output_filename = os.path.join(output_dir, output_filename)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

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

        tiff_prefix = tiff_hash(wkt_geometry, resolution)

        outputs = []
        for feature in self._features:
            output_filename = f"{tiff_prefix}_{self._layer_name}_{feature.name}.tiff"
            if output_dir:
                output_filename = os.path.join(output_dir, output_filename)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

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
