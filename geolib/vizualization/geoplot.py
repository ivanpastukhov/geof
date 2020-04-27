import logging
from bokeh.plotting import figure, show
from bokeh.models import HoverTool
from bokeh.tile_providers import CARTODBPOSITRON, get_provider


logger = logging.getLogger('geolib.features.utils')
logger.setLevel(logging.DEBUG)

class GeoPlot:
    # TODO: добавить других провайдеров
    def __init__(self):
        # self.provider = get_provider(CARTODBPOSITRON)
        # self.x = None
        # self.y = None
        # self.default_size = 4
        # self.default_color = 'blue'
        # self.default_category = None
        self.tooltips = [
            ("index", "$index"),
            ("(x,y)", "($x, $y)")
        ]
        return

    # def _build_source(self, x, y, size, color, category):
    #     source = {
    #         'x': x,
    #         'y': y,
    #         'size': self.default_size,
    #         'color': self.default_color
    #     }
    #     if size is not None:
    #         source['size'] = size
    #     if color is not None:
    #         source['color'] = color
    #     if category is not None:
    #         source['category'] = category
    #     return source

    def _build_tooltips(self, category):
        if category is not None:
            self.tooltips.append(('category', '@category'))
        return self.tooltips

    def __add_hover(self, p, tooltips):
        hover = HoverTool(tooltips=tooltips)
        p.add_tools(hover)
        p.hover.point_policy = 'follow_mouse'
        return p

    def plot_points(self, x, y, size=4, color='blue', category=None):
        # source = self._build_source(x, y, size, color, category)
        tooltips = self._build_tooltips(category)
        p = figure(x_range=(min(x), max(x)),
                   y_range=(min(y), max(y)),
                   x_axis_type='mercator',
                   y_axis_type='mercator',
                   )
        p = self.__add_hover(p, tooltips)
        p.add_tile(get_provider(CARTODBPOSITRON))
        p.circle(x=x,
                 y=y,
                 size=size,
                 fill_color=color,
                 line_color=color,
                 )
        show(p)
        return




# class GeoPlot:
#     # TODO: добавить других провайдеров
#     def __init__(self):
#         self.provider = get_provider(CARTODBPOSITRON)
#         return
#
#     def plot(self, x, y, **kwargs):
#         """
#         :param kwargs:
#         :return:
#         """
#         p = figure(x_range=(min(x), max(x)),
#                    y_range=(min(y), max(y)),
#                    x_axis_type='mercator',
#                    y_axis_type='mercator')
#         p.add_tile(self.provider)
#         p.circle(**kwargs)
#         p.hover.point_policy = 'follow_mouse'
#         show(p)
#         return
