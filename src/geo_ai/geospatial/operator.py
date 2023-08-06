from typing import Optional, List, Callable

from src.geo_ai.geospatial.exceptions import UnacceptableCRSException
from src.geo_ai.geospatial.geospatial_file_manager import GeospatialFileManager
from src.geo_ai.geospatial.vector import FeatureCollection, intersect_feature_collections


# TODO write this so that particular validations can be added over time and then evaluated at a particular time
class GeospatialOperationValidator:
    def __init__(self):
        self.validations: List[Callable] = []
    
    def add_crs_validation(self):
        self.validations.append(self._assert_acceptable_crs)
        return self

    def _assert_acceptable_crs(self, feature_collections: List[FeatureCollection]) -> None:
        try:
            assert all(feature_collection.crs == feature_collections[0].crs for feature_collection in feature_collections)
        except AssertionError:
            raise UnacceptableCRSException(f"Unacceptable CRS; all feature collection must be in the same CRS.")

    def validate_feature_collections(self, feature_collections: List[FeatureCollection]) -> bool:
        for validation in self.validations:
            validation(feature_collections)


class GeospatialOperator:
    def __init__(
            self,
            geospatial_file_manager: GeospatialFileManager,
            geospatial_operation_validator: GeospatialOperationValidator,
                 ):
        self.geospatial_file_manager = geospatial_file_manager
        self.geospatial_operation_validator = geospatial_operation_validator

    def validate(self, feature_collections: List[FeatureCollection]) -> None:
        self.geospatial_operation_validator.add_crs_validation()
        self.geospatial_operation_validator.validate_feature_collections(feature_collections)

    def intersect(
            self,
            input_filepaths: List[str],
            output_filepath: Optional[str] = "output.geojson"
    ) -> None:
        feature_collections = [
            self.geospatial_file_manager.read_file_to_feature_collection(input_filepath) 
            for input_filepath in input_filepaths
        ]
        self.validate(feature_collections)
        intersection = intersect_feature_collections(feature_collections)

        output_feature_collection = FeatureCollection.from_shape(
            intersection, feature_collections[0].crs, feature_collections[0].schema, "0", {}
        )

        self.geospatial_file_manager.write_file_from_feature_collection(output_filepath, output_feature_collection)