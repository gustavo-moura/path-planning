import collections
import math

from genetic.utils import pairwise_circle, _normal, _eq_line, _eq_intersection_point

# CartesianPoint = collections.namedtuple('CartesianPoint', 'x y')
GeoPoint = collections.namedtuple("GeoPoint", "latitude, longitude, altitude")
Version = collections.namedtuple("Version", "major, minor")


class CartesianPoint:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"


class Mapa:
    def __init__(self, origin, destination, areas_n, inflation_rate=0.1):
        self.origin = origin  # CartesianPoint : Define o ponto de partida da rota
        self.destination = (
            destination  # CartesianPoint : Define o ponto de destino da rota
        )
        self.areas_n = areas_n  # [area, ...]
        # area = [CartesianPoint(),...]
        self.areas_n_inf = [
            self._inflate_area(area, inflation_rate=inflation_rate) for area in areas_n
        ]

    def _inflate_area(self, area, inflation_rate):

        lines = []

        for V1, V2 in pairwise_circle(area):
            N = _normal(V1, V2)

            NV1 = CartesianPoint(
                V1.x + N.x * inflation_rate, V1.y + N.y * inflation_rate
            )
            NV2 = CartesianPoint(
                V2.x + N.x * inflation_rate, V2.y + N.y * inflation_rate
            )

            a, b, c = _eq_line(NV1, NV2)
            lines.append((a, b, c))

            # if verbose:
            #     print(f"V1:{NV1} V2:{NV2}  ->  L:({a}x + {b}y + {c} = 0)")

        new_area = []

        for L1, L2 in pairwise_circle(lines):
            x, y = _eq_intersection_point(L1[0], L1[1], L1[2], L2[0], L2[1], L2[2])
            new_area.append(CartesianPoint(x, y))

            # if verbose:
            #     print(
            #         f"L1:({L1[0]}x + {L1[1]}y + {L1[2]} = 0) L2:({L2[0]}x + {L2[1]}y + {L2[2]} = 0)  ->  V=({x},{y})"
            #     )

        return new_area


class Conversor:
    def list_geo_to_cart(l, geo_home):
        for i in l:
            yield Conversor.geo_to_cart(i, geo_home)

    def list_cart_to_geo(l, geo_home):
        for i in l:
            yield Conversor.cart_to_geo(i, geo_home)

    def geo_to_cart(geo_point, geo_home):
        def calc_y(lat, lat_):
            return (lat - lat_) * (10000000.0 / 90)

        def calc_x(longi, longi_, lat_):
            return (longi - longi_) * (
                6400000.0 * (math.cos(lat_ * math.pi / 180) * 2 * math.pi / 360)
            )

        x = calc_x(geo_point.longitude, geo_home.longitude, geo_home.latitude)
        y = calc_y(geo_point.latitude, geo_home.latitude)

        # return CartesianPoint(x, y, geo_point.altitude)
        return CartesianPoint(x, y)

    def cart_to_geo(cartesian_point, geo_home):
        def calc_latitude_y(lat_, y):
            return ((y * 90) / 10000000.0) + lat_

        def calc_longitude_x(lat_, longi_, x):
            return ((x * 90) / (10008000 * math.cos(lat_ * math.pi / 180))) + longi_

        longitude_x = calc_longitude_x(
            geo_home.latitude, geo_home.longitude, cartesian_point.x
        )
        latitude_y = calc_latitude_y(geo_home.latitude, cartesian_point.y)

        # return GeoPoint(longitude_x, latitude_y, cartesian_point.z)
        return GeoPoint(longitude_x, latitude_y, 10)
