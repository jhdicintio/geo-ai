import pytest

@pytest.fixture
def test_boulder_geojson_filepath() -> str:
    return "tests/fixtures/geospatial/vector/boulder.geojson"


@pytest.fixture
def test_denver_geojson_filepath() -> str:
    return "tests/fixtures/geospatial/vector/denver.geojson"

