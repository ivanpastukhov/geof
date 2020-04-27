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

    def plot(self, x, y, idx, category=None, size=None):
        data = {
            'id': idx,
            'x': x,
            'y': y
        }
        tooltips = [
            ('id', '@id')
        ]
        if category is not None:
            data['category'] = category
            tooltips.append(('category', '@category'))
        p = figure(x_range=(min(x), max(x)),
                   y_range=(min(y), max(y)),
                   x_axis_type='mercator',
                   y_axis_type='mercator',
                   tooltips=tooltips)
        p.add_tile(self.provider)
        if size is not None:
            data['size'] = size
            p.circle('x', 'y', size='size', source=data)
        else:
            p.circle('x', 'y', source=data)
        p.hover.point_policy = 'follow_mouse'
        show(p)
        return
