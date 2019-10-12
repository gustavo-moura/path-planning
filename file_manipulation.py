

# KML Google Earth .kml
# -------------------------------------------------------------------
'''
Faz a criação do arquivo KML para poder fazer a visualização da rota
final no Google Earth.

@param routes
@param mission
@throws FileNotFoundException
'''
def save_kml(filename, routes, mission): #throws FileNotFoundException
    complete_filename = filename + 'mission.kml'
    
    with open(complete_filename, 'w+') as file: 

        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        file.write("<kml>")
        file.write("<Document>")
        file.write("<name>Barragem.kml</name>")
        file.write("<name>Barragem.kml</name>")
        file.write("<Folder>")
        file.write("<name>Barragem</name>")
        file.write("<open>1</open>")
       
        count = 0
        for route in routes:
            save_kml_geo_route(route.geo_route, file, "route" + str(count))
            count += 1 
        
        save_kml_point(file, mission.area.geo_home, "H")

        count = 0
        for geo_point in mission.area.geo_points:
            save_kml_point(file, geo_point, "P"+ str(count))
            count += 1

        file.write("</Folder>")
        file.write("</Document>")
        file.write("</kml>")

    return complete_filename


def save_kml_geo_route(self, geo_route, file, name): 
    file.write("<Placemark>")
    file.write("<name>" + name + "</name>")
    file.write("<styleUrl>#m_ylw-pushpin0000</styleUrl>")
    file.write("<LineString>")
    file.write("<tessellate>1</tessellate>")
    file.write("<altitudeMode>relativeToGround</altitudeMode>")
    file.write("<coordinates>")

    for waypoint in geo_route:
        file.write("{},{},{}\n".format(waypoint.longitude, waypoint.latitude, waypoint.height))

    file.write("</coordinates>")
    file.write("</LineString>")
    file.write("</Placemark>")


def save_kml_point(file, point, name):

    file.write("<Placemark>")
    file.write("<name>{}</name>".format(name))
    '''
    file.write("<LookAt>")
    out.printf("<longitude>-53.28548239302506</longitude>\n")
    file.write("<latitude>-29.44866075195521</latitude>")
    file.write("<altitude>0</altitude>")
    file.write("<heading>88.09967918418015</heading>")
    file.write("<tilt>49.55113510360746</tilt>")
    file.write("<range>384.2069866108237</range>")
    file.write("<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>")
    file.write("</LookAt>")
    '''
    file.write("<styleUrl>#m_ylw-pushpin</styleUrl>")
    file.write("<Point>")
    file.write("<gx:drawOrder>1</gx:drawOrder>")
    file.write("<altitudeMode>relativeToGround</altitudeMode>")
    file.write("<coordinates>{},{},{}</coordinates>".format(point.longitude, point.latitude, point.height))
    file.write("</Point>")
    file.write("</Placemark>")



# Mavros .wp
# -------------------------------------------------------------------
def save_mavros(filename, routes): #throws FileNotFoundException
    count = 1

    for route in routes:
        #with open(path + '_mavros' + str(count) + '.wp', 'w+') as file: # ToDo: definir path 
        with open(filename + '.wp', 'w+') as file:
            #file.write("latitude,longitude,altitude(m),heading(deg),curvesize(m),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(m),poi_altitudemode,photo_timeinterval\n")
            current_waypoint = 1

            file.write('QGC WPL 120\n') # Determines the file version

            i = 0

            for geo_point in route.geo_route:
                file.write(
                    str(i) + '\t'
                    + str(current_waypoint) + '\t' 
                    + '3\t16\t3\t0\t0\t0\t'
                    + '{:10.8f}'.format(geo_point.latitude) + '\t' 
                    + '{:10.8f}'.format(geo_point.longitude) + '\t'
                    + '{:10.8f}'.format(geo_point.height) + '\t'
                    + '1'
                    + '\n'
                )

                current_waypoint = 0
                i+=1





# Litchi
# -------------------------------------------------------------------
# ToDo: NAO TESTADO AINDA
def save_litchi(filename, routes, mission): #throws FileNotFoundException
    count = 1

    for route in routes:
        with open(path + '_route' + str(count) + '.csv', 'w+') as file: # ToDo: definir path 
            file.write("latitude,longitude,altitude(m),heading(deg),curvesize(m),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(m),poi_altitudemode,photo_timeinterval\n")

            for geo_point in route.geo_route:
                file.write(str(geo_point.latitude) + ',' 
                    + str(geo_point.longitude) + ',' # era latitude tbm
                    + str(Controller.calc_heading_cartesian(mission.area.points[0], mission.area.points[1])) + ','
                    + "0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1"
                    + '\n'
                )

