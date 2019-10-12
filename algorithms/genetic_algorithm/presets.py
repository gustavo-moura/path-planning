import os
import sys
nb_dir = os.path.split(os.getcwd())[0]
if nb_dir not in sys.path:
    sys.path.append(nb_dir)


import data_definitions  as pp
from utils import controller


class Map:
    def __init__(self, origem, destino, bonificadoras, penalizadoras, nao_navegaveis):
        self.origem = origem                    # CartesianPoint
        self.destino = destino                  # CartesianPoint
        self.bonificadoras = bonificadoras      # [Area, ...]
        self.penalizadoras = penalizadoras      # [Area, ...]
        self.nao_navegaveis = nao_navegaveis    # [Area, ...]
        self.geo_home = pp.GeoPoint((-47.932949, -22.002467, 0))

    def get_geo_points(self):
        geo_points = []

        for area in self.bonificadoras + self.penalizadoras + self.nao_navegaveis:
            geo_points += area.geo_points

        # print("\ngeo_points: ")
        # print(geo_points)
        return geo_points


# C2 Atrás do bloco do ICMC
def build_area_C2_bonificadora():
    geo_home = pp.GeoPoint((-47.932949, -22.002467, 0))

    points = [
        (-47.932749, -22.002332, 7), 
        (-47.932794, -22.002177, 13), 
        (-47.932664, -22.002147, 13), 
        (-47.932612, -22.002306, 7)
    ]

    geo_points = [pp.GeoPoint(i) for i in points]

    area = pp.Area(geo_home, geo_points)

    return area


def build_area_C2_penalizadora():
    geo_home = pp.GeoPoint((-47.932949, -22.002467, 0))

    points = [
        (-47.932099, -22.002278, 20),
        (-47.932063, -22.002396, 20),
        (-47.932772, -22.002582, 20),
        (-47.932811, -22.002465, 20)
    ]

    geo_points = [pp.GeoPoint(i) for i in points]

    area = pp.Area(geo_home, geo_points)

    return area



def build_map_C2():
    geo_home = pp.GeoPoint((-47.932949, -22.002467, 0))

    origem = controller.to_cartesian(pp.GeoPoint((-47.932546, -22.002237, 15)), geo_home)

    destino = controller.to_cartesian(pp.GeoPoint((-47.932608, -22.002674, 13)), geo_home)

    b1 = build_area_C2_bonificadora()
    bonificadoras = [b1]


    p1 = build_area_C2_penalizadora()
    penalizadoras = [p1]


    nao_navegaveis = []


    mapa = Map(origem, destino, bonificadoras, penalizadoras, nao_navegaveis)


    return mapa



def transform_geo_points(points, home):
    cartesian_route = [pp.CartesianPoint(point[0], point[1], 10) for point in points]
    return controller.transform_geo_points(cartesian_route, home) 


def new_geo_point(tupler):
    return pp.GeoPoint(tupler)