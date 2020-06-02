

class GeoPoint:
    """A geographical point.
        Args:
            latitude (float): value of point expressed in latitude geographical coordinate (specifies north-south position on earth surface).
            longitude (float): value of point expressed in longitude geographical coordinate (specifies east-west position on earth surface).
            altitude (float): value of point expressed in absolute altitude (distance above sea level).
    """

    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __repr__(self):
        return f"[{self.latitude}, {self.longitude}, {self.altitude}]"

    def to_cartesian(self, geo_home):
    """Converts this geographical point to a Cartesian point.

    Args:
        self (GeoPoint)
        geo_home (GeoPoint): a reference GeoPoint to specify the (0,0,0) coordinate in the Cartesian system. While converting many points, they must use the same reference geo_home.

    Returns:
        (CartesianPoint): the corresponding Cartesian point for this GeoPoint
    """
        def calc_y(lat, lat_):
            return (lat - lat_) * (10000000.0 / 90)

        def calc_x(longi, longi_, lat_):
            return (longi - longi_) * (6400000.0 * (math.cos(lat_ * math.pi / 180) * 2 * math.pi / 360))

        x = calc_x(self.longitude, geo_home.longitude, geo_home.latitude)
        y = calc_y(self.latitude, geo_home.latitude)

        # return CartesianPoint(x, y, geo_point.altitude)  # TODO: 3D - to transform this point to 3D
        return CartesianPoint(x, y)


class CartesianPoint:
    """A Cartesian point.
        Args:
            x (float): value of point on X-axis.
            y (float): value of point on Y-axis.
            z (float): value of point on Z-axis.
    """

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"


    def to_geo(cartesian_point, geo_home):
    """Converts this Cartesian point to a geographical point.

    Args:
        self (CartesianPoint)
        geo_home (GeoPoint): a reference GeoPoint to specify the (0,0,0) coordinate in the Cartesian system. While converting many points, they must use the same reference geo_home.

    Returns:
        (GeoPoint): the corresponding GeoPoint for this CartesianPoint.
    """
        def calc_latitude_y(lat_, y):
            return ((y * 90) / 10000000.0) + lat_

        def calc_longitude_x(lat_, longi_, x):
            return ((x * 90) / (10008000 * math.cos(lat_ * math.pi / 180))) + longi_

        longitude_x = calc_longitude_x(geo_home.latitude, geo_home.longitude, cartesian_point.x)
        latitude_y = calc_latitude_y(geo_home.latitude, cartesian_point.y)

        # return GeoPoint(longitude_x, latitude_y, cartesian_point.z)
        return GeoPoint(longitude_x, latitude_y, 10)


class Mapa:
    def __init__(
        self, 
        origin, 
        destination, 
        areas_n=None, 
        areas_b=None, 
        inflation_rate=0.1
    ):
        self.origin = origin  # CartesianPoint : Define o ponto de partida da rota
        self.destination = destination  # CartesianPoint : Define o ponto de destino da rota
        self.areas_n = areas_n  # [area, ...] : Areas nao-navegaveis
        #                       # area = [CartesianPoint(),...]
        self.areas_n_inf = [self._inflate_area(area, inflation_rate=inflation_rate) for area in areas_n]

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