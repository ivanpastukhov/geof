import logging
from bokeh.plotting import figure, show
from bokeh.tile_providers import CARTODBPOSITRON, get_provider


logger = logging.getLogger('geolib.features.utils')
logger.setLevel(logging.DEBUG)


class GeoPlot:
    # TODO: добавить других провайдеров
    def __init__(self):
        self.provider = get_provider(CARTODBPOSITRON)
        return

    def plot(self, x, y, **kwargs):
        """
        :param kwargs:
        :return:
        """
        p = figure(x_range=(min(x), max(x)),
                   y_range=(min(y), max(y)),
                   x_axis_type='mercator',
                   y_axis_type='mercator')
        p.add_tile(self.provider)
        p.circle(**kwargs)
        p.hover.point_policy = 'follow_mouse'
        show(p)
        return
