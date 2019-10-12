import collections

import math

GeoPoint = collections.namedtuple('GeoPoint', 'latitude, longitude, altitude')
CartesianPoint = collections.namedtuple('CartesianPoint', 'x, y, z')

def calc_heading_geo(p1, p2, home):
    c1 = to_cartesian(p1, home)
    c2 = to_cartesian(p2, home)

    heading = math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi + 90 # ToDo: verificar
    return heading


def transform_geo_points(route, home):
    '''
    Transforma um linkedList de pontos cartesianos para um linkedList de
    pontos geográficos.

    @param route
    @param home
    @return
    '''
    final_route = []

    for element in route:
        final_route.append(to_geo_point(element, home))

    return final_route


def to_geo_point(cartesian_point, home):
    longitude_x = calc_longitude_x(home.latitude, home.longitude, cartesian_point.x)
    latitude_y = calc_latitude_y(home.latitude, cartesian_point.y)

    return GeoPoint(latitude_y, longitude_x, cartesian_point.z)


def to_cartesian(geo_point, home):
    x = calc_x(geo_point.longitude, home.longitude, home.latitude)
    y = calc_y(geo_point.latitude, home.latitude)

    return CartesianPoint(x, y, geo_point.altitude)


def to_cartesians(geo_point_list, home):
    return [to_cartesian(point, home) for point in geo_point_list]


def calc_y(lat, lat_):
    return (lat - lat_) * (10000000.0 / 90)


def calc_x(longi, longi_, lat_):
    pi = math.pi
    return (longi - longi_) * (6400000.0 * (math.cos(lat_ * pi / 180) * 2 * pi / 360)) # ToDo: verificar math


def calc_latitude_y(lat_, y):
    return ((y * 90) / 10000000.0) + lat_


def calc_longitude_x(lat_, longi_, x):
    return ((x * 90) / (10008000 * math.cos(lat_ * math.pi / 180))) + longi_


# def photo_lenght_on_ground(picture_distance, camera_opening):
#     return 2 * picture_distance * math.tan((camera_opening / 2) * math.pi / 180)


# def calc_heading_cartesian(c1, c2):
#     heading = 360 - math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi 

#     heading = heading % 360 #if heading>360 else heading # ToDo: simplificar com expressão de cima

#     if verbose:
#         print("%5.2f %5.2f %5.2f\n", c1.x, c1.y, c1.z)
#         print("%5.2f %5.2f %5.2f\n", c2.x, c2.y, c2.z)
#         print("dx = %5.2f \n", (c2.x - c1.x))
#         print("dy = %5.2f \n", (c2.y - c1.y))
#         print("dy/dx = %5.2f \n", (c2.y - c1.y) / (c2.x - c1.x))
#         print("dy/dx = %5.2f \n", math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi)

#         print(heading)

#     return heading
