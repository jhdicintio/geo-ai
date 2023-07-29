import pytest

from typing import Generator

from src.geo_ai.local_file_reader import LocalFileReader

@pytest.fixture
def test_geojson_path() -> str:
    yield "tests/fixtures/geospatial/vector/boulder.geojson"

@pytest.fixture
def subject() -> Generator[LocalFileReader, None, None]:
    yield LocalFileReader()


def read_geospatial_file_test(subject, test_geojson_path): 
    result = subject.read_geospatial_file(test_geojson_path)
    assert result == None
