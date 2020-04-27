import overpy
from pyproj import Transformer
import logging
import numpy as np

logger = logging.getLogger('geolib.features.utils')
logger.setLevel(logging.DEBUG)


# TODO: добавить проверку статуса на сервере OSM
class OverpassWrapper:
    def __init__(self):
        self.api = overpy.Overpass()
        self.data = None
        self.nodes = None
        self.ways = None
        self.relations = None
        return

    def request_data(self, query):
        return self.api.query(query)

    def _parse_nodes(self, nodes):
        mapping = lambda x: dict(
            {
                'id': x.id,
                'item_type': 'node',
                'lat': safe_cast(x.lat, float),
                'lon': safe_cast(x.lon, float),
                'attributes': x.attributes
            },
            **x.tags)
        return map(mapping, nodes)

    def _parse_ways(self, ways):
        # TODO: парсить ноды в ways
        mapping = lambda x: dict(
            {
                'id': x.id,
                'item_type': 'way',
                'lat': safe_cast(x.center_lat, float),
                'lon': safe_cast(x.center_lon, float),
                'attributes': x.attributes
            },
            **x.tags)
        return map(mapping, ways)

    def _parse_relations(self, relations):
        # TODO: парсить мемберов
        mapping = lambda x: dict(
            {
                'id': x.id,
                'item_type': 'relation',
                'lat': safe_cast(x.center_lat, float),
                'lon': safe_cast(x.center_lon, float),
                'attributes': x.attributes
            },
            **x.tags)
        return map(mapping, relations)

    def parse_response(self, data):
        self.nodes = data.nodes
        self.ways = data.ways
        self.relations = data.relations
        res = [
            *self._parse_nodes(self.nodes),
            *self._parse_ways(self.ways),
            *self._parse_relations(self.relations)
        ]
        return res


class SRCTransformer:
    def __init__(self, source_crs="EPSG:4326", target_crs="EPSG:3857"):
        """Transforms SRC.
        # EPSG:3857 - Web Mercator, Google Web Mercator, Spherical Mercator,
         WGS 84 Web Mercator или WGS 84 / Pseudo-Mercator
        # EPSG:4326 - WGS 84 -- WGS84 - World Geodetic System 1984, used in GPS
        """
        # TODO: дополнить другими SRC
        if source_crs != "EPSG:4326" or target_crs != "EPSG:3857":
            raise NotImplementedError('Only "EPSG:4326" to "EPSG:3857" conversion is supported at the moment.')
        self.transformer = Transformer.from_crs(source_crs, target_crs)

    def transform(self, lat, lon):
        """Transforms SRC from EPSG:4326 (WGS84) to EPSG:3857 (Web Mercator)"""
        return self.transformer.transform(lat, lon)


def safe_cast(value, to_type, default=np.NaN):
    try:
        return to_type(value)
    except(ValueError, TypeError):
        return default



