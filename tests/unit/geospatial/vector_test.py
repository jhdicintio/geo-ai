import pytest

from shapely import Geometry

from src.geo_ai.geospatial.geospatial_file_manager import GeospatialFileManager
from src.geo_ai.geospatial.vector import FeatureCollection, intersect_feature_collections

DEGREE2_ERROR_THRESHOLD = 0.01

@pytest.fixture
def test_boulder_feature_collection(test_boulder_geojson_filepath: str) -> FeatureCollection:
    return GeospatialFileManager().read_file_to_feature_collection(test_boulder_geojson_filepath)

@pytest.fixture
def test_denver_feature_collection(test_denver_geojson_filepath: str) -> FeatureCollection:
    return GeospatialFileManager().read_file_to_feature_collection(test_denver_geojson_filepath)


def feature_collection_to_shape_should_not_alter_polygon_test(test_boulder_feature_collection):
    assert test_boulder_feature_collection.to_shape() == test_boulder_feature_collection.features[0].shape


def intersect_feature_collections_test(test_boulder_feature_collection, test_denver_feature_collection):
    intersection = intersect_feature_collections(
        (test_denver_feature_collection, test_boulder_feature_collection)
    )
    assert isinstance(intersection, Geometry)
    assert intersection.symmetric_difference(test_boulder_feature_collection.to_shape()).area < DEGREE2_ERROR_THRESHOLD
