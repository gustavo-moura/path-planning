import collections
import math

CartesianPoint = collections.namedtuple('CartesianPoint', 'x y')
GeoPoint = collections.namedtuple('GeoPoint', 'latitude, longitude, altitude')

class Mapa():
    def __init__(self, origin, destination, areas_n, inflation_rate=0.1):
        self.origin = origin           # CartesianPoint : Define o ponto de partida da rota
        self.destination = destination # CartesianPoint : Define o ponto de destino da rota
        #self.areas_n = areas_n        # [area, ...]
                                       # area = [CartesianPoint(),...]      
        self.areas_n_inf = [ self._inflate_area(area, inflation_rate=inflation_rate) for area in areas_n ]
        
        
    def _inflate_area(self, area, inflation_rate=0):
        # Infla uma área retangular em uma porcentagem do tamanho, alterando os valores em x% de cada vértice
        
        x = area[2].x - area[0].x
        y = area[1].y - area[3].y
        
        inc = (inflation_rate)
        dec = -(inflation_rate)
        
        new_area = [
            CartesianPoint(area[0].x + dec * x, area[0].y + dec * y), # left,  bottom
            CartesianPoint(area[1].x + dec * x, area[1].y + inc * y), # left,  top
            CartesianPoint(area[2].x + inc * x, area[2].y + inc * y), # right, top
            CartesianPoint(area[3].x + inc * x, area[3].y + dec * y)  # right, bottom
        ]
        new_area.append(new_area[0]) # Repetir primeiro ponto, para o ignore do shape na hora de plotar
        
        return new_area


class Conversor():

    def list_geo_to_cart(self, l, geo_home):
        for i in l:
            yield self.geo_to_cart(i, geo_home)

    def list_cart_to_geo(self, l, geo_home):
        for i in l:
            yield self.cart_to_geo(i, geo_home)


    def geo_to_cart(self, geo_point, geo_home):
        
        def calc_y(lat, lat_):
            return (lat - lat_) * (10000000.0 / 90)
        def calc_x(longi, longi_, lat_):
            return (longi - longi_) * (6400000.0 * (math.cos(lat_ * math.pi / 180) * 2 * math.pi / 360))


        x = calc_x(geo_point.longitude, home.longitude, home.latitude)
        y = calc_y(geo_point.latitude, home.latitude)

        return CartesianPoint(x, y, geo_point.altitude)


    def cart_to_geo(self, cartesian_point, geo_home):

        def calc_latitude_y(lat_, y):
            return ((y * 90) / 10000000.0) + lat_
        def calc_longitude_x(lat_, longi_, x):
            return ((x * 90) / (10008000 * math.cos(lat_ * math.pi / 180))) + longi_


        longitude_x = calc_longitude_x(home.latitude, home.longitude, cartesian_point.x)
        latitude_y = calc_latitude_y(home.latitude, cartesian_point.y)

        return GeoPoint((longitude_x, latitude_y, cartesian_point.z))