import overpass
from pyproj import Transformer

class OverpassWrapper:
    def __init__(self):
        return

    ## Показать доступные теги
    # def ...

    ## Загрузить объекты (ноды, узлы) для выбранного тега/тегов
    # def ...

    ## Распарсить датку с апишки
    # def ...

class SRC_Transformer:
    def __init__(self, source_crs="EPSG:4326", target_crs="EPSG:3857"):
        """Transforms SRC.
        # EPSG:3857 - Web Mercator, Google Web Mercator, Spherical Mercator, WGS 84 Web Mercator или WGS 84 / Pseudo-Mercator
        # EPSG:4326 - WGS 84 -- WGS84 - World Geodetic System 1984, used in GPS
        """
        #TODO: дополнить другими SRC
        if source_crs != "EPSG:4326" or target_crs != "EPSG:3857":
            raise NotImplementedError('Only "EPSG:4326" to "EPSG:3857" conversion is supported at the moment.')
        self.transformer = Transformer.from_crs(source_crs, target_crs)

    def transform(self, lat, lon):
        return self.transformer.transform(lat, lon)





class GeoTools:
    def __init__(self):

        return
