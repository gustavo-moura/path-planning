import collections
import math

from src.naboo.utils import pairwise_circle, _normal, _eq_line, _eq_intersection_point

CartesianPoint = collections.namedtuple("CartesianPoint", "x y")
GeoPoint = collections.namedtuple("GeoPoint", "latitude, longitude, altitude")
Vector = collections.namedtuple("Vector", "x y")
Version = collections.namedtuple("Version", "major, minor")


class Mapa:
    def __init__(
        self, origin, destination, areas_n=None, areas_b=None, inflation_rate=0.1
    ):
        self.origin = origin  # CartesianPoint : Define o ponto de partida da rota
        self.destination = (
            destination  # CartesianPoint : Define o ponto de destino da rota
        )
        self.areas_n = areas_n  # [area, ...] : Areas nao-navegaveis
        #                       # area = [CartesianPoint(),...]
        self.areas_n_inf = [
            self._inflate_area(area, inflation_rate=inflation_rate) for area in areas_n
        ]

        self.areas_b = areas_b  # [area, ...] : Areas bonificadoras

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


# class Mapa():
#     def __init__(self, origin, destination, areas_n, inflation_rate=0.1, mode='scalar'):
#         self.origin = origin           # CartesianPoint : Define o ponto de partida da rota
#         self.destination = destination # CartesianPoint : Define o ponto de destino da rota
#         self.areas_n = areas_n         # [area, ...]
#                                        # area = [CartesianPoint(),...]
#         self.areas_n_inf = [ self._inflate_area(area, inflation_rate=inflation_rate, mode=mode) for area in areas_n ]


#     def _inflate_area(self, area, inflation_rate, mode):
#         if mode == 'percentage':
#             # Infla uma área retangular em uma porcentagem do tamanho, alterando os valores em x% de cada vértice
#             x = area[2].x - area[0].x
#             y = area[1].y - area[3].y

#             inc = (inflation_rate)
#             dec = -(inflation_rate)

#             new_area = [
#                 CartesianPoint(area[0].x + dec * x, area[0].y + dec * y), # left,  bottom
#                 CartesianPoint(area[1].x + dec * x, area[1].y + inc * y), # left,  top
#                 CartesianPoint(area[2].x + inc * x, area[2].y + inc * y), # right, top
#                 CartesianPoint(area[3].x + inc * x, area[3].y + dec * y)  # right, bottom
#             ]
#             new_area.append(new_area[0]) # Repetir primeiro ponto, para o ignore do shape na hora de plotar

#         elif mode == 'scalar':
#             # Infla uma área retangular em uma quantidade fixa
#             inc = (inflation_rate)
#             dec = -(inflation_rate)

#             new_area = [
#                 CartesianPoint(area[0].x + dec, area[0].y + dec), # left,  bottom
#                 CartesianPoint(area[1].x + dec, area[1].y + inc), # left,  top
#                 CartesianPoint(area[2].x + inc, area[2].y + inc), # right, top
#                 CartesianPoint(area[3].x + inc, area[3].y + dec)  # right, bottom
#             ]
#             new_area.append(new_area[0]) # Repetir primeiro ponto, para o ignore do shape na hora de plotar

#         return new_area


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
