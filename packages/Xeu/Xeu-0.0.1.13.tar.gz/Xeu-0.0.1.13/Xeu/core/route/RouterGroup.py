# _*_ coding:utf-8 _*_
import copy

__all__ = ['RouterGroup']


class RouterGroup(object):

    def __init__(self, group=None, route_map=None):

        self.route_map = route_map is not None and route_map or {}

        if isinstance(route_map, RouterGroup):
            if route_map.url_map:
                self.route_map = copy.deepcopy(route_map.url_map)
        elif isinstance(route_map, dict):
            if route_map == {}:
                raise ValueError('route_map must not be empty')
        else:
            raise ValueError('route_map must be dict')

        if self.route_map:
            for app, url in self.route_map.items():
                if url != '' and group not in [None, '']:
                    if url.startswith('/'):
                        self.__group = '/' + group
                    else:
                        self.__group = '/' + group + '/'
                    self.route_map[app] = self.__group + url
                else:
                    if url.startswith('/'):
                        self.route_map[app] = url
                    else:
                        self.route_map[app] = '/' + url

    def __add__(self, other):
        if not isinstance(other, RouterGroup) and not other.url_map:
            raise ValueError('type r-reference must be RouterGroup')
        mix = self.route_map.keys() & other.url_map.keys()
        if mix:
            raise ValueError('must not exist mix-key like %s' % str(mix))

        __add_dic = dict()
        __add_dic.update(other.url_map)
        __add_dic.update(self.route_map)
        return RouterGroup(route_map=__add_dic)

    @property
    def url_map(self):
        return self.route_map

    def __repr__(self):
        return str(self.route_map)

    def to_dict(self):
        return self.route_map

