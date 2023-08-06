from typing import Dict

import fiona
from fiona.crs import from_string
from shapely.geometry import shape, mapping

from src.geo_ai.geospatial.exceptions import UnsupportedDriverException
from src.geo_ai.geospatial.vector import Feature, FeatureCollection

# TODO add additional driver support
SUPPORTED_DRIVERS: Dict[str, str] = {
    "geojson": "GeoJSON",
    # ".shp": "ESRI Shapefile",
    # ".gpkg": "GPKG"
}


class GeospatialFileManager:
    def read_file_to_feature_collection(self, filepath: str) -> FeatureCollection:
        with fiona.open(filepath, 'r') as src:
            features = [
                   Feature(
                        id=feature.id,
                        shape=shape(feature['geometry']),
                        properties=feature.properties
                    ) for feature in src
            ]
            feature_collection = FeatureCollection(
                schema=src.schema,
                crs=src.crs.to_string(),
                features=features
            )                
        return feature_collection
    
    def _determine_driver(self, filepath: str) -> str:
        suffix = filepath.split(".")[-1]
        try: 
            return SUPPORTED_DRIVERS[suffix]
        except KeyError as err:
            raise UnsupportedDriverException(f"No supported driver for {suffix} files yet.")

    
    def write_file_from_feature_collection(self, filepath: str, feature_collection: FeatureCollection) -> None:
        driver = self._determine_driver(filepath)

        with fiona.open(
            filepath, 
            'w',
            crs=from_string(feature_collection.crs),
            driver=driver, 
            schema=feature_collection.schema
            ) as dest:
            for feature in feature_collection.features:
                dest.write(
                    {'id': feature.id, 'geometry': mapping(feature.shape), 'properties':feature.properties}
                    )
