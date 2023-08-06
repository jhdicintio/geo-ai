import json
from typing import Generator

import pytest
from shapely.geometry import Polygon
from src.geo_ai.geospatial.exceptions import UnsupportedDriverException

from src.geo_ai.geospatial.geospatial_file_manager import GeospatialFileManager


@pytest.fixture
def subject() -> Generator[GeospatialFileManager, None, None]:
    yield GeospatialFileManager()


def read_file_to_feature_collection_test(subject, test_boulder_geojson_filepath: str):
    feature_collection = subject.read_file_to_feature_collection(test_boulder_geojson_filepath)
    assert feature_collection.schema == {'geometry': 'Polygon', 'properties': {}}
    assert feature_collection.crs == "EPSG:4326"
    assert feature_collection.features[0].id == '0'
    assert isinstance(feature_collection.features[0].shape, Polygon)
    assert feature_collection.features[0].properties == {}    


def determine_driver_success_test(subject, test_boulder_geojson_filepath):
    driver = subject._determine_driver(test_boulder_geojson_filepath)
    assert driver == "GeoJSON"


def determine_driver_unsupported_driver_test(subject):
    with pytest.raises(UnsupportedDriverException):
        subject._determine_driver("fake/file/foo.bar")


def write_file_from_feature_collection_test(subject, test_boulder_geojson_filepath: str):
    output_filepath = "tests/fixtures/geospatial/vector/test.geojson"
    feature_collection = subject.read_file_to_feature_collection(test_boulder_geojson_filepath)
    
    subject.write_file_from_feature_collection(output_filepath, feature_collection)

    assert json.load(open(test_boulder_geojson_filepath, 'r')) == json.load(open(output_filepath, 'r'))
