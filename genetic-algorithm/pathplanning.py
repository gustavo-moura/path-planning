import math


class Map()

	def __init__(self, bonificadoras, penalizadoras, nao_navegaveis):
		self.bonificadoras = bonificadoras
		self.penalizadoras = penalizadoras
		self.nao_navegaveis = nao_navegaveis


class GeoPoint():

    def __init__(self, tupler):
        self.longitude = tupler[0]
        self.latitude = tupler[1]
        self.altitude = tupler[2]
		


class Area():

    def __init__(self, geo_home, geo_points):

        self.geo_home = geo_home
        self.geo_points = geo_points
        self.home = self.to_cartesian(geo_home, geo_home) 
        self.points = self.to_cartesians(geo_points, geo_home) # points = [p1, p2, p3, p4]


    def to_geo_point(cartesian_point, home):
        longitude_x = self.calc_longitude_x(home.latitude, home.longitude, cartesian_point.x)
        latitude_y = self.calc_latitude_y(home.latitude, cartesian_point.y)

        return GeoPoint((longitude_x, latitude_y, cartesian_point.z))


    def to_cartesian(geo_point, home):
        x = self.calc_x(geo_point.longitude, home.longitude, home.latitude)
        y = self.calc_y(geo_point.latitude, home.latitude)

        return CartesianPoint(x, y, geo_point.height)

    def to_cartesians(geo_point_list, home):
        return [self.to_cartesian(point, home) for point in geo_point_list]


    def calc_y(lat, lat_):
        return (lat - lat_) * (10000000.0 / 90)


    def calc_x(longi, longi_, lat_):
        pi = math.pi
        return (longi - longi_) * (6400000.0 * (math.cos(lat_ * pi / 180) * 2 * pi / 360))


    def calc_latitude_y(lat_, y):
        return ((y * 90) / 10000000.0) + lat_


    def calc_longitude_x(lat_, longi_, x):
        return ((x * 90) / (10008000 * math.cos(lat_ * math.pi / 180))) + longi_


