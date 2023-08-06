import os
import pytest 

from typing import Generator

from src.geo_ai.geospatial.exceptions import UnacceptableCRSException
from src.geo_ai.geospatial.geospatial_file_manager import GeospatialFileManager
from src.geo_ai.geospatial.vector import FeatureCollection
from src.geo_ai.geospatial.operator import GeospatialOperationValidator, GeospatialOperator


@pytest.fixture
def fake_feature_collection_4326() -> FeatureCollection:
    return FeatureCollection(
        schema={},
        crs="EPSG:4326",
        features=[]
    )


@pytest.fixture
def fake_feature_collection_3857() -> FeatureCollection:
    return FeatureCollection(
        schema={},
        crs="EPSG:3857",
        features=[]
    )


@pytest.fixture
def validator_subject() -> Generator[GeospatialOperationValidator, None, None]:
    yield GeospatialOperationValidator()


@pytest.fixture
def operator_subject() -> Generator[GeospatialOperator, None, None]:
    yield GeospatialOperator(GeospatialFileManager(), GeospatialOperationValidator())

def _assert_acceptable_crs_should_return_true_when_acceptable_test(
        validator_subject: GeospatialOperationValidator,
        fake_feature_collection_4326: FeatureCollection
        ):
    validator_subject._assert_acceptable_crs(feature_collections=[fake_feature_collection_4326, fake_feature_collection_4326])


def _assert_acceptable_crs_should_fail_when_unacceptable_test(
        validator_subject: GeospatialOperationValidator,
        fake_feature_collection_3857: FeatureCollection,
        fake_feature_collection_4326: FeatureCollection
        ):
    with pytest.raises(UnacceptableCRSException):
        validator_subject._assert_acceptable_crs(feature_collections=[fake_feature_collection_3857, fake_feature_collection_4326])


def intersect_with_default_ouput_location_test(
        operator_subject: GeospatialOperator,
        test_boulder_geojson_filepath: str,
        test_denver_geojson_filepath: str
):
    operator_subject.intersect([test_boulder_geojson_filepath, test_denver_geojson_filepath])

    feature_collection = GeospatialFileManager().read_file_to_feature_collection("output.geojson")
    print(vars(feature_collection))
    assert feature_collection.crs == "EPSG:4326"
    assert feature_collection.schema == {'properties': {}, 'geometry': 'Polygon'}
    assert len(feature_collection.features) == 1
    assert feature_collection.features[0].shape.__geo_interface__ == {'coordinates': (((-105.2380192130085, 39.994736266609834), (-105.26164475547756, 39.994736266609834), (-105.26164475547756, 40.009593133467376), (-105.2380192130085, 40.009593133467376), (-105.2380192130085, 39.994736266609834)),), 'type': 'Polygon'}
    assert feature_collection.features[0].id == "0"
    assert feature_collection.features[0].properties == {}
    
    os.remove("output.geojson")