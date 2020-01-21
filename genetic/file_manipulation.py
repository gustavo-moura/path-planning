import json

from genetic.data_definitions import GeoPoint, Conversor


def read_mapa(mapa_filename, mapa_id):

    with open(mapa_filename, "r") as mapa_file:
        mapa_file = json.load(mapa_file)
        mapa = mapa_file[mapa_id]

        geo_home = GeoPoint(
            mapa["geo_home"][1], mapa["geo_home"][0], mapa["geo_home"][2]
        )

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


# KML Google Earth .kml
# -------------------------------------------------------------------
"""
Faz a criação do arquivo KML para poder fazer a visualização da rota
final no Google Earth.
@param routes
@param mission
"""


def save_kml(filename, routes, areas):
    complete_filename = filename + "mission.kml"

    with open(complete_filename, "w+") as file:

        file.write('<?xml version="1.0" encoding="UTF-8"?>')
        file.write("<kml>")
        file.write("<Document>")
        file.write("<name>Barragem.kml</name>")
        file.write("<name>Barragem.kml</name>")
        file.write("<Folder>")
        file.write("<name>Barragem</name>")
        file.write("<open>1</open>")

        count = 0
        for route in routes:
            save_kml_geo_route(file, route, "route_" + str(count))
            count += 1

        # save_kml_point(file, area.geo_home, "H")

        for area in areas:
            count = 0
            for geo_point in area:
                save_kml_point(file, geo_point, "P" + str(count))
                count += 1

        file.write("</Folder>")
        file.write("</Document>")
        file.write("</kml>")

    return complete_filename


def save_kml_geo_route(self, file, geo_route, name):
    file.write("<Placemark>")
    file.write("<name>" + name + "</name>")
    file.write("<styleUrl>#m_ylw-pushpin0000</styleUrl>")
    file.write("<LineString>")
    file.write("<tessellate>1</tessellate>")
    file.write("<altitudeMode>relativeToGround</altitudeMode>")
    file.write("<coordinates>")

    for waypoint in geo_route:
        file.write(
            "{},{},{}\n".format(
                waypoint.longitude, waypoint.latitude, waypoint.altitude
            )
        )

    file.write("</coordinates>")
    file.write("</LineString>")
    file.write("</Placemark>")


def save_kml_point(file, point, name):

    file.write("<Placemark>")
    file.write("<name>{}</name>".format(name))
    """
    file.write("<LookAt>")
    out.printf("<longitude>-53.28548239302506</longitude>\n")
    file.write("<latitude>-29.44866075195521</latitude>")
    file.write("<altitude>0</altitude>")
    file.write("<heading>88.09967918418015</heading>")
    file.write("<tilt>49.55113510360746</tilt>")
    file.write("<range>384.2069866108237</range>")
    file.write("<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>")
    file.write("</LookAt>")
    """
    file.write("<styleUrl>#m_ylw-pushpin</styleUrl>")
    file.write("<Point>")
    file.write("<gx:drawOrder>1</gx:drawOrder>")
    file.write("<altitudeMode>relativeToGround</altitudeMode>")
    file.write(
        "<coordinates>{},{},{}</coordinates>".format(
            point.longitude, point.latitude, point.altitude
        )
    )
    file.write("</Point>")
    file.write("</Placemark>")


# Mavros .wp
# -------------------------------------------------------------------
# WRITE
# ______________________________________________


def write_mavros(filename, geo_points):  # throws FileNotFoundException
    print("Writing mavros file...\nMake sure the filename given has the .wp extension")
    with open(filename, "w+") as file:
        current_waypoint = 1

        file.write("QGC WPL 120\n")  # Determines the file version

        i = 0

        for geo_point in geo_points:
            file.write(
                str(i)
                + "\t"
                + str(current_waypoint)
                + "\t"
                + "3\t16\t3\t0\t0\t0\t"
                + "{:10.8f}".format(geo_point.longitude)
                + "\t"
                + "{:10.8f}".format(geo_point.latitude)
                + "\t"
                + "{:10.8f}".format(geo_point.altitude)
                + "\t"
                + "1"
                + "\n"
            )

            current_waypoint = 0
            i += 1

    print("Output file generated: {}".format(filename))
