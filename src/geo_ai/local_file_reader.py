from typing import Any

import fiona
from shapely.geometry import shape

class LocalFileReader:
    def read_file(self, filepath: str) -> Any:
        with fiona.open(filepath, 'r') as src:
            shapes = [
                shape(feature['geometry']) for feature in src
            ]
        return shapes
        