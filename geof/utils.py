import overpass
import overpy
from pyproj import Transformer
import pandas as pd
import logging
import numpy as np

logger = logging.getLogger('geof.utils')
logger.setLevel(logging.DEBUG)


## TODO: добавить проверку статуса на сервере OSM
class OverpassWrapper:
    def __init__(self):
        self.api = overpy.Overpass()
        return

    def request_data(self, query):
        self.data = self.api.query(query)

    def parse_nodes(self, nodes):
        mapping = lambda x: dict(
            {
                'id': x.id,
                'lat': self._safe_cast(x.lat, float),
                'lon': self._safe_cast(x.lon, float),
                'attributes': x.attributes
            },
            **x.tags)
        return map(mapping, nodes)

    def parse_ways(self, ways):
        ## TODO: парсить ноды в ways
        mapping = lambda x: dict(
            {
                'id': x.id,
                'lat': self._safe_cast(x.center_lat, float),
                'lon': self._safe_cast(x.center_lon, float),
                'attributes': x.attributes
            },
            **x.tags)
        return map(mapping, ways)

    def parse_relations(self, relations):
        ## TODO: парсить мемберов
        mapping = lambda x: dict(
            {
                'id': x.id,
                'lat': self._safe_cast(x.center_lat, float),
                'lon': self._safe_cast(x.center_lon, float),
                'attributes': x.attributes
            },
            **x.tags)
        return map(mapping, relations)

    def parse_response(self, data):
        self.nodes = data.nodes
        self.ways = data.ways
        self.relations = data.relations
        res = [
            *self.parse_nodes(self.nodes),
            *self.parse_ways(self.ways),
            *self.parse_relations(self.relations)
        ]
        return res

    @staticmethod
    def _safe_cast(value, to_type, default=np.NaN):
        try:
            return to_type(value)
        except(ValueError, TypeError):
            return default



    # TODO: тесты на корректность парсинга
    @staticmethod
    def overpass_to_df(features, droplevel_level=0, droplevel_axis=1):
        """
        Parse data from Overpass API to pandas.DataFrame
        :param features: array-like
        :return:
        pandas.DataFrame
        """
        colnames_expected = ['type', 'id', 'geometry', 'properties']
        df = pd.DataFrame(features)
        # парсим json'ы внутри датафрейма
        if not all(name in df.columns for name in colnames_expected):
            logger.warning(f'Colnames are expected: {colnames_expected}, but passed: {df.columns}')
        df = df.agg({'type': lambda x: x, 'id': lambda x: x, 'geometry': pd.Series, 'properties': pd.Series})
        if (droplevel_axis != None) and (droplevel_level != None):
            df = df.droplevel(level=droplevel_level, axis=droplevel_axis)
        return df


class SRC_Transformer:
    def __init__(self, source_crs="EPSG:4326", target_crs="EPSG:3857"):
        """Transforms SRC.
        # EPSG:3857 - Web Mercator, Google Web Mercator, Spherical Mercator, WGS 84 Web Mercator или WGS 84 / Pseudo-Mercator
        # EPSG:4326 - WGS 84 -- WGS84 - World Geodetic System 1984, used in GPS
        """
        # TODO: дополнить другими SRC
        if source_crs != "EPSG:4326" or target_crs != "EPSG:3857":
            raise NotImplementedError('Only "EPSG:4326" to "EPSG:3857" conversion is supported at the moment.')
        self.transformer = Transformer.from_crs(source_crs, target_crs)

    def transform(self, lat, lon):
        """Transforms SRC from EPSG:4326 (WGS84) to EPSG:3857 (Web Mercator)"""
        return self.transformer.transform(lat, lon)
