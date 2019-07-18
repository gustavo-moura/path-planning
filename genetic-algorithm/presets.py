# --------------- Points
'''
Pen0
(-47.932099, -22.002278, 20)

Pen1
(-47.932063, -22.002396, 20)

Pen2
(-47.932772, -22.002582, 20)

Pen3
(-47.932811, -22.002465, 20)

Dest
(-47.932608, -22.002674, 13)

Orig
(-47.932546, -22.002237, 15)

P0
(-47.932749, -22.002332, 7)

P1
(-47.932794, -22.002177, 13)

P2 
(-47.932664, -22.002147, 13)

P3 
(-47.932612, -22.002306, 7)
'''

import pathplanning as pp


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

	b1 = build_area_C2_bonificadora()
	bonificadoras = [b1]


	p1 = build_area_C2_penalizadora()
	penalizadoras = [p1]


	nao_navegaveis = []


	mapa = pp.Map(bonificadoras, penalizadoras, nao_navegaveis)


	return mapa

