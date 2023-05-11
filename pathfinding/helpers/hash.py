import hashlib


def bgt_hash(wkt_geometry: str) -> str:
    h = hashlib.new("sha256")
    h.update(wkt_geometry.encode())
    return h.hexdigest()[:8]


def gpkg_hash(wkt_geometry: str) -> str:
    h = hashlib.new("sha256")
    h.update(wkt_geometry.encode())
    return h.hexdigest()[:8]


def tiff_hash(wkt_geometry: str, resolution: float) -> str:
    diversifier = f"{wkt_geometry} {resolution}"
    h = hashlib.new("sha256")
    h.update(diversifier.encode())
    return h.hexdigest()[:8]
