import math

path='' # ToDo: melhorar
verbose = False # flag to print heading calculation

class Area():

    def __init__(self, geo_home, geo_points):

        self.geo_home = geo_home
        self.geo_points = geo_points
        self.home = Controller.to_cartesian(geo_home, geo_home) # ToDo: ???
        self.points = Controller.to_cartesians(geo_points, geo_home) # points = [p1, p2, p3, p4]
        self.hypotenuse = self.calc_hypotenuse(self.points)
        self.base_lenght = self.calc_base_lenght(self.points)


    def calc_hypotenuse(self, points):
        h1 = points[3].minus(points[0])
        h2 = points[2].minus(points[1])

        return max(h1.norm(), h2.norm())
    
    def calc_base_lenght(self, points):
        h1 = points[3].minus(points[2])
        h2 = points[0].minus(points[1])

        return max(h1.norm(), h2.norm())
    '''
    private static double calcHipotenusa(CartesianPoint p1, CartesianPoint p2, CartesianPoint p3, CartesianPoint p4) {
        CartesianPoint h1 = p4.minus(p1)
        CartesianPoint h2 = p3.minus(p2)
        return Math.max(h1.norm(), h2.norm())
    }

    private double calcComprimentoBase(CartesianPoint p1, CartesianPoint p2, CartesianPoint p3, CartesianPoint p4) {
        CartesianPoint h1 = p4.minus(p3)
        CartesianPoint h2 = p1.minus(p2)
        return Math.max(h1.norm(), h2.norm())
    }
    '''


class Camera():

    def __init__(self, open_angle, resolution, 
        max_zoom, shutter_time, mega_pixel,
        trigger, weight, sensor, 
        focus_distance):

        self.open_angle = open_angle # open_angle = (h,w)
        self.resolution = resolution # resolution = (h,w)
        self.max_zoom = max_zoom
        self.shutter_time = shutter_time
        self.mega_pixel = mega_pixel
        self.trigger = trigger
        self.weight = weight
        self.sensor = sensor # sensor = (x,y)
        self.focus_distance = focus_distance


class CartesianPoint():

    id_number = None
    id_count = 0

    def __init__(self, x,y,z):
        self.x = x # position relative to base, in meters
        self.y = y # position relative to base, in meters
        self.z = z # height in meters


    # Distance between two points, in meters
    def minus(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z

        return CartesianPoint(x, y, z)

    # Sum between two cartesian points
    def plus(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z

        return CartesianPoint(x, y, z)


    # Divide the cartesian point by a number
    '''
    P3 = P1 / number Divide um vetor grande em partes pequenas para a
    formação da rota.
    '''
    def divide(self, number):
        x = self.x / number
        y = self.y / number
        z = self.z / number

        return CartesianPoint(x, y, z)

    '''
    Adiciona no ponto atual com um outro ponto multiplicado por um
     * coeficiente. P3 = P1 + coef * P2 P3 é o resultado a ser retornado P1 é o
     * objeto atual ao qual foi chamado a função P2 é o objeto passado como
     * parâmetro.
    '''
    def sumproduct(self, coef, other):
        x = self.x + coef * other.x
        y = self.y + coef * other.y
        z = self.z + coef * other.z

        return CartesianPoint(x, y, z)


    def norm(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


class Drone():

    def __init__(self, weight, min_battery, 
        max_battery, max_velocity, 
        efficient_velocity):

        #self.name = name
        self.weight = weight
        self.min_battery = min_battery
        self.max_battery = max_battery
        self.max_velocity = max_velocity
        self.efficient_velocity = efficient_velocity

 
class GeoPoint():

    #def __init__(self, longitude, latitude, height):   
        # self.longitude = longitude
        # self.latitude = latitude
        # self.height = height
    def __init__(self, tupler):
        self.longitude = tupler[0]
        self.latitude = tupler[1]
        self.height = tupler[2]

class Mission():
    HORIZONTAL_DIRECTION = 1
    VERTICAL_DIRECTION = 2
    UP_MOVEMENT = 3
    DOWN_MOVEMENT = 4

    def __init__(self, direction, movement, drone, 
        camera, area, SD_card, 
        picture_distance, zoom, 
        sobrePosicao, blur_factor):

        self.direction = direction  # int
        self.movement = movement    # int
        self.drone = drone          # Drone
        self.camera = camera        # Camera
        self.area = area            # Area
        self.SD_card = SD_card      # double
        self.picture_distance = picture_distance # double
        self.zoom = zoom            # double
        self.sobrePosicao = sobrePosicao # double # ToDo: rename
        self.blur_factor = blur_factor #double


        self.width = self.photo_length_on_ground(picture_distance, camera.open_angle[1]) # ToDo: melhorar # ToDo: melhorar tipo de dado do camera.open_angle['w']
        self.height = self.photo_length_on_ground(picture_distance, camera.open_angle[0]) # ToDo: melhorar tipo de dado do camera.open_angle['w']

        self.velocity_shutter = self.width * self.blur_factor / (camera.resolution[0] * camera.shutter_time) # ToDo: melhorar tipo de dado do camera.open_angle['w']
        self.velocity_cruiser = min(drone.efficient_velocity / 3.6, self.velocity_shutter) # ToDo: ver de onde vem esse 3.6

        if direction == self.HORIZONTAL_DIRECTION:
            self.picture_precision = self.width * 1000 / camera.resolution[1] # ToDo: melhorar tipo de dado do camera.open_angle['w']
            self.turn_qty = self.calc_turn_qty(area.hypotenuse, self.height, self.sobrePosicao) # ToDo: renomear
            self.turn_width = area.hypotenuse / (self.turn_qty-1)
            self.turn_lenght = area.base_lenght

        else:
            self.picture_precision = self.height * 1000 / camera.resolution[0] # ToDo: melhorar tipo de dado do camera.open_angle['w']
            self.turn_qty = self.calc_turn_qty(area.base_lenght, self.width, self.sobrePosicao) # ToDo: renomear
            self.turn_width = area.base_lenght / (self.turn_qty-1)
            self.turn_lenght = area.hypotenuse


    # Calculate the turns quantity
    def calc_turn_qty(self, hypotenuse, width, sobrePosicao):
        return (0.8 + hypotenuse / (width * (1 - sobrePosicao))) + 1

    def photo_length_on_ground(self, picture_distance, camera_opening):
        return 2 * picture_distance * math.tan((camera_opening / 2) * math.pi / 180)


class Route():

    def __init__(self, route, mission):
        self.route = route
        self.geo_route = Controller.transform_geo_points(route, mission.area.geo_home) #ToDo: checar essa função
        self.route_length = Controller.calc_route_length(route)

        if mission.direction == mission.HORIZONTAL_DIRECTION:
            measure = mission.width
        else:
            measure = mission.height

        self.picture_qty = round(self.route_length / (measure * (1 - mission.sobrePosicao)))   
        self.flight_duration = (self.route_length / mission.velocity_cruiser)
        self.picture_per_second = self.picture_qty / self.flight_duration
            


    def save_kml(self, file, name): # ToDo: corrigir
        file.write("<Placemark>")
        file.write("<name>" + name + "</name>")
        file.write("<styleUrl>#m_ylw-pushpin0000</styleUrl>")
        file.write("<LineString>")
        file.write("<tessellate>1</tessellate>")
        file.write("<altitudeMode>relativeToGround</altitudeMode>")
        file.write("<coordinates>")
        #print('##############################################################################\n')
        for waypoint in self.geo_route:
            file.write("{},{},{}\n".format(waypoint.longitude, waypoint.latitude, waypoint.height))

        #print('##############################################################################\n')
        #file.write(this.geoRoute.stream().map(e -> e.toString()).reduce(String::concat).get()) # ToDo: checar e corrigir
        file.write("</coordinates>")
        file.write("</LineString>")
        file.write("</Placemark>")


class Controller():
    

    def __init__(self, mission):
        self.mission = mission


    '''
    /**
     * Transforma os pontos geográficos da missão em pontos cartesianos em
     * metros para efetuar o cálculo da rota. Após isso, é calculado os pontos
     * da rota que o drone irá fazer com base no número de voltas para fazer o
     * mapeamento completo da área. Então é transformado de pontos cartesianos
     * da rota em metros para pontos geográficos e adionados na lista final.
     *
     * @return
     */
    '''
    def calc_complete_route(self):
        mission = self.mission
        area = mission.area

        # All measures are cartesian, except for those explicitly saying that are geographical, with the prefix "geo_"
        home = area.home
        points = area.points

        route = [] #List of CartesianPoints


        if mission.direction == Mission.HORIZONTAL_DIRECTION:
            if mission.movement == Mission.UP_MOVEMENT:
                A = 0
                B = 1
                C = 2
                D = 3

            else:
                A = 3
                B = 2
                C = 1
                D = 0

        else:
            if mission.direction == Mission.UP_MOVEMENT:
                A = 0
                B = 3
                C = 2
                D = 1

            else:
                A = 2
                B = 1
                C = 0
                D = 3


        route.append(area.home)

        # Generalizing
        r_bar = points[C].minus(points[B]).divide(mission.turn_qty - 1)
        l_bar = points[D].minus(points[A]).divide(mission.turn_qty - 1)

        route.append(points[A])
        route.append(points[B])


        for i in range(int(mission.turn_qty)):
            if i%2 == 0:
                route.append(points[A].sumproduct(i, l_bar))
                route.append(points[B].sumproduct(i, r_bar))

            else:
                route.append(points[B].sumproduct(i, r_bar))
                route.append(points[A].sumproduct(i, l_bar))


        route.append(home)

        return Route(route, mission)


    def calc_route(self): #throws FileNotFoundException, IOException
        route = self.calc_complete_route()
        mission = self.mission

        print("-------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------")
        print("Quantidade de voltas: " + str(mission.turn_qty))
        print("Quantidade de WayPoints: " + str(len(route.route)))
        print("Comprimento da volta: " + str(mission.turn_lenght))
        print("Largura da volta: " + str(mission.turn_width))
        print("Width da foto: " + str(mission.width))
        print("Height da foto: " + str(mission.height))
        print("Hipotenusa: " + str(mission.area.hypotenuse))
        print("Comprimento da base: " + str(mission.area.base_lenght))
        print("Comprimento total da rota: " + str(route.route_length) + "metros")
        print("-------------------------------------------------------------------------------")
        print("P0: " + str(mission.area.points[0]))
        print("P1: " + str(mission.area.points[1]))
        print("P2: " + str(mission.area.points[2]))
        print("P3: " + str(mission.area.points[3]))
        print("Quantidade de Fotos: " + str(route.picture_qty))
        print("Velocity Shutter: " + str(mission.velocity_shutter))
        print("Velocity Cruiser: " + str(mission.velocity_cruiser))
        print("Flight Time: " + str(route.flight_duration / 60))
        print("Pictures Per Second: " + str(route.picture_per_second))
        print("Pictures Precision: " + str(mission.picture_precision))
        print("Precisão em milimetros: " + str(Controller.calc_GSD(mission)))
        print("-------------------------------------------------------------------------------")

        routes = [] #List of CartesianPoints

        if mission.drone.min_battery < route.flight_duration:
            mission_qty = math.ceil((route.flight_duration / 60) / mission.drone.min_battery) # ToDo: verificar essa função da math

            index = Controller.split_index(route.route, mission_qty) # ToDo: verificar essa função

            index.insert(0, 1) # addFirst(1)
            index.insert(len(index), len(route.route)-2) # addLast(len(route.route) - 2)


            for m in range(mission_qty):
                sub_route = Controller.build_sub_route(route.route, index[m], index[m + 1]) # Controller.build_sub_route(route.route, index.get(m), index.get(m + 1))
                sub_route.insert(0, mission.area.home) # addFirst(mission.area.home)
                sub_route.insert(len(sub_route), mission.area.home) # addLast(mission.area.home)
                
                sub = Route(sub_route, mission)

                print("----------------------------------------------(SubRoute ", m, ")---------------------------------------------------")
                print("Número de WayPoints: ", len(sub_route))
                print("Comprimento da rota: ", sub.route_length)
                print("Número de Fotos ", sub.picture_qty)
                print("Flight Time ", sub.flight_duration / 60)
                print("Pictures Per Second ", sub.picture_per_second)
                #print(sub.geoRoute.stream().map(e -> e.toString()).reduce(String::concat).get()) # ToDo: verificar função

                routes.append(sub)

            else:
                routes.append(route)


            Controller.save_kml(routes, mission)
            Controller.save_litchi(routes, mission)


    # Original function
    def save_litchi_original(routes, mission): #throws FileNotFoundException
        count = 1

        for route in routes:
            with open(path + 'route' + str(count) + '.csv', 'w+') as file: # ToDo: definir path 
                file.write("latitude,longitude,altitude(m),heading(deg),curvesize(m),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(m),poi_altitudemode,photo_timeinterval\n")

                for geo_point in route.geo_route:
                    file.write(str(geo_point.latitude) + ',' 
                        + str(geo_point.longitude) + ',' # era latitude tbm
                        + str(Controller.calc_heading_cartesian(mission.area.points[0], mission.area.points[1])) + ','
                        + "0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1"
                        + '\n'
                    )

    # Format for MAVROS
    def save_litchi(routes, mission): #throws FileNotFoundException
        count = 1

        for route in routes:
            with open(path + 'mavros' + str(count) + '.wp', 'w+') as file: # ToDo: definir path 
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


    def save_kml_point(file, point, name):

        file.write("<Placemark>")
        file.write("<name>{}</name>".format(name))
        '''
        //        file.write("<LookAt>")
        //        out.printf("<longitude>-53.28548239302506</longitude>\n")
        //        file.write("<latitude>-29.44866075195521</latitude>")
        //        file.write("<altitude>0</altitude>")
        //        file.write("<heading>88.09967918418015</heading>")
        //        file.write("<tilt>49.55113510360746</tilt>")
        //        file.write("<range>384.2069866108237</range>")
        //        file.write("<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>")
        //        file.write("</LookAt>")
        '''
        file.write("<styleUrl>#m_ylw-pushpin</styleUrl>")
        file.write("<Point>")
        file.write("<gx:drawOrder>1</gx:drawOrder>")
        file.write("<altitudeMode>relativeToGround</altitudeMode>")
        # file.write("<coordinates>{:1.15f},{:1.15f},{:1.15f}</coordinates>".format(point.longitude, point.latitude, point.height))
        file.write("<coordinates>{},{},{}</coordinates>".format(point.longitude, point.latitude, point.height))
        file.write("</Point>")
        file.write("</Placemark>")


    '''
    /**
     * Faz a criação do arquivo KML para poder fazer a visualização da rota
     * final no Google Earth.
     *
     * @param routes
     * @param misison
     * @throws FileNotFoundException
     */
    '''
    def save_kml(routes, mission): #throws FileNotFoundException

        with open(path + 'mission.kml', 'w+') as file: 

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
                route.save_kml(file, "route" + str(count))
                count += 1 
            
            Controller.save_kml_point(file, mission.area.geo_home, "H")

            count = 0
            for geo_point in mission.area.geo_points:
                Controller.save_kml_point(file, geo_point, "P"+ str(count))
                count += 1

            file.write("</Folder>")
            file.write("</Document>")
            file.write("</kml>")


    def calc_heading_cartesian(c1, c2):
        heading = 360 - math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi # ToDo: verificar

        heading = heading % 360 #if heading>360 else heading # ToDo: simplificar com expressão de cima

        if verbose:
            print("%5.2f %5.2f %5.2f\n", c1.x, c1.y, c1.z)
            print("%5.2f %5.2f %5.2f\n", c2.x, c2.y, c2.z)
            print("dx = %5.2f \n", (c2.x - c1.x))
            print("dy = %5.2f \n", (c2.y - c1.y))
            print("dy/dx = %5.2f \n", (c2.y - c1.y) / (c2.x - c1.x))
            print("dy/dx = %5.2f \n", math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi) # ToDo: verificar

            print(heading)

        return heading


    def calc_heading_geo(p1, p2, home):
        c1 = to_cartesian(p1, home)
        c2 = to_cartesian(p2, home)

        heading = math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi + 90 # ToDo: verificar
        return heading


    def calc_route_length(route):
        total_length = 0

        iter_route = iter(route)
        
        current = route[0] # route.getFirst()

        for element in route[1:]:
            print('    current', current.x)
            print('    element', element.x)
            total_length += element.minus(current).norm()
            print('    total_length', total_length)
            current = element

        return total_length


    def build_sub_route(route, first_i, last_i):
        res = []
        for i in range(first_i, last_i):
            res.append(route[i])

        return res


    def split_index(route, mission_qty):

        size = math.floor(len(route) / mission_qty)

        res = []

        for m in range(1, mission_qty):
            res.append(size * m)

        return res


    '''
    /**
     * Transforma um linkedList de pontos cartesianos para um linkedList de
     * pontos geográficos.
     *
     * @param route
     * @param home
     * @return
     */
    '''
    def transform_geo_points(route, home):
        final_route = []

        for element in route:
            final_route.append(Controller.to_geo_point(element, home))

        return final_route


    def to_geo_point(cartesian_point, home):
        longitude_x = Controller.calc_longitude_x(home.latitude, home.longitude, cartesian_point.x)
        latitude_y = Controller.calc_latitude_y(home.latitude, cartesian_point.y)

        return GeoPoint((longitude_x, latitude_y, cartesian_point.z))


    def to_cartesian(geo_point, home):
        x = Controller.calc_x(geo_point.longitude, home.longitude, home.latitude)
        y = Controller.calc_y(geo_point.latitude, home.latitude)

        return CartesianPoint(x, y, geo_point.height)

    def to_cartesians(geo_point_list, home):
        return [Controller.to_cartesian(point, home) for point in geo_point_list]



    def calc_y(lat, lat_):
        return (lat - lat_) * (10000000.0 / 90)


    def calc_x(longi, longi_, lat_):
        pi = math.pi
        return (longi - longi_) * (6400000.0 * (math.cos(lat_ * pi / 180) * 2 * pi / 360)) # ToDo: verificar math


    def calc_latitude_y(lat_, y):
        return ((y * 90) / 10000000.0) + lat_


    def calc_longitude_x(lat_, longi_, x):
        return ((x * 90) / (10008000 * math.cos(lat_ * math.pi / 180))) + longi_


    def photo_lenght_on_ground(picture_distance, camera_opening):
        return 2 * picture_distance * math.tan((camera_opening / 2) * math.pi / 180)


    def calc_denescala(mission): # ToDo: renomear
        return mission.picture_distance / (mission.camera.focus_distance * (10**-3))


    def calc_sensor_x(mission): # ToDo: simplificar
        return mission.camera.sensor[0] / mission.camera.resolution[1]

    def calc_sensor_y(mission):
        return mission.camera.sensor[1] / mission.camera.resolution[1]

    def calc_tam(mission):
        a = Controller.calc_sensor_x(mission)
        b = Controller.calc_sensor_y(mission)

        return min(a, b) # ToDo: verificar

    def calc_GSD(mission):
        denescala = Controller.calc_denescala(mission)
        tam = Controller.calc_tam(mission)
        print(str(denescala) + "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        return denescala * tam






























