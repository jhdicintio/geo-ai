from shapely import Geometry
from rasterio.crs import CRS

class Boundary:
    def __init__(shape: Geometry, crs: CRS):
        self.shape = shape
        self.crs = CRS

    