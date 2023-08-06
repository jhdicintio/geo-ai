from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from shapely import Geometry
from shapely.ops import unary_union
from shapely import intersection_all


@dataclass
class Feature:
    id: str
    shape: Geometry
    properties: Optional[Dict[str, Any]]


class FeatureCollection:
    def __init__(self, schema: Dict[str, Any], crs: str, features: List[Feature]):
        self.schema: Dict[str, Any] = schema
        self.crs: str = crs
        self.features: List[Feature] = features

    def to_shape(self) -> Geometry:
        return unary_union([
            feature.shape for feature in self.features
        ])
    
    @classmethod
    def from_shape(
        cls, 
        shape: Geometry,
        crs: str,
        schema: Dict[str, Any],
        id: str,
        properties: Dict[str, Any]=None
        ):
        return cls(
            schema=schema,
            crs=crs,
            features=[
                Feature(
            id=id, shape=shape, properties=properties
                )
            ]
        )


def intersect_feature_collections(feature_collections: List[FeatureCollection]) -> Geometry:
    """
    TODO: no rounding error
    """ 
    return intersection_all([feature_collection.to_shape() for feature_collection in feature_collections])
