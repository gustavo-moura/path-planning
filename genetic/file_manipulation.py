from genetic.data_definitions import GeoPoint, Conversor


def upload_mapa(mapa_file, mapa_id):
    mapa = mapa_file[mapa_id]

    geo_home = GeoPoint(mapa["geo_home"][1], mapa["geo_home"][0], mapa["geo_home"][2])

    areas_bonificadoras = [
        Conversor.list_geo_to_cart(area["geo_points"], geo_home)
        for area in mapa["areas_bonificadoras"]
    ]
    areas_penalizadoras = [
        Conversor.list_geo_to_cart(area["geo_points"], geo_home)
        for area in mapa["areas_penalizadoras"]
    ]

    areas_nao_navegaveis = []
    for area in mapa["areas_nao_navegaveis"]:
        geo_points = []
        for geo_point in area["geo_points"]:
            geo_points.append(
                Conversor.geo_to_cart(
                    GeoPoint(geo_point[1], geo_point[0], geo_point[2]), geo_home
                )
            )
        geo_points.append(geo_points[0])
        areas_nao_navegaveis.append(geo_points)

    return geo_home, areas_bonificadoras, areas_penalizadoras, areas_nao_navegaveis
