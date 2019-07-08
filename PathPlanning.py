import math

class Area():

    def __init__(self, geo_home, geo_points):

        self.geo_home = geo_home
        self.geo_points = geo_points
        self.home = Controller.to_cartesian(geo_home) # ToDo: ???
        self.points = to_cartesian(geo_points) # points = [p1, p2, p3, p4]
        self.hypotenuse = calc_hypotenuse(points)
        self.base_lenght = calc_base_lenght(points)


    def calc_hypotenuse(self, point):
        pass
    
    def calc_base_lenght(self, point):
        pass
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
    def sumproduct(self, number):
        x = self.x + coef * other.x
        y = self.y + coef * other.y
        z = self.z + coef * other.z

        return CartesianPoint(x, y, z)


    def norm():
        return sqrt(x**2 + y**2 + z**2)


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

    def __init__(longitude, latitude, height):
        
        self.longitude = longitude
        self.latitude = latitude
        self.height = height


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


        self.width = Controller.photo_lenght_on_ground(picture_distance, camera.open_angle['w']) # ToDo: melhorar
        self.height = photo_lenght_on_ground(picture_distance, camera.open_angle['h'])

        self.velocity_shutter = self.width * self.blur_factor / (camera.resolution['w'] * camera.shutter_time)
        self.velocity_cruiser = min(drone.efficient_velocity / 3.6, velocity_shutter) # ToDo: ver de onde vem esse 3.6

        if direction == HORIZONTAL_DIRECTION:
            self.picture_precision = self.width * 1000 / camera.resolution['w']
            self.turn_qty = calc_turn_qty(area.hypotenuse, self.height, self.sobrePosicao) # ToDo: renomear
            self.turn_width = area.hypotenuse / (turn_qty-1)
            self.turn_lenght = area.base_lenght

        else:
            self.picture_precision = self.height * 1000 / camera.resolution['h']
            self.turn_qty = calc_turn_qty(area.base_lenght, self.width, self.sobrePosicao) # ToDo: renomear
            self.turn_width = area.base_lenght / (turn_qty-1)
            self.turn_lenght = area.hypotenuse


        # Calculate the turns quantity
        def calc_turn_qty(hypotenuse, width, sobrePosicao):
            return (0.8 + hypotenuse / (width * (1 - sobrePosicao))) + 1

        def photo_length_on_ground(picture_distance, camera_opening):
            return 2 * picture_distance * math.tan((camera_opening / 2) * math.pi / 180)


class Route():

    def __init__():
        self.route = route
        self.geo_route = transform_geo_point(route, mission.area.home) #ToDo: checar essa função
        self.route_length = calc_route_length(route)

        if mission.direction == HORIZONTAL_DIRECTION:
            self.picture_qty = math.round(route_length / (mission.width * (1 - sobrePosicao)))
            self.flight_duration = (route_length / mission.velocity_cruiser)
            self.picture_per_second = picture_qty / flight_duration


    def saveKml(file, name): # ToDo: corrigir
        file.write("<Placemark>")
        file.write("<name>" + name + "</name>")
        file.write("<styleUrl>#m_ylw-pushpin0000</styleUrl>")
        file.write("<LineString>")
        file.write("<tessellate>1</tessellate>")
        file.write("<altitudeMode>relativeToGround</altitudeMode>")
        file.write("<coordinates>")
        #file.write(this.geoRoute.stream().map(e -> e.toString()).reduce(String::concat).get()) # ToDo: checar e corrigir
        file.write("</coordinates>")
        file.write("</LineString>")
        file.write("</Placemark>")


class Controller():
    pass

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
    def calc_complete_route():
        mission = self.mission
        area = mission.area

        # All measures are cartesian, except for those explicitly saying that are geographical, with the prefix "geo_"
        home = area.home
        points = area.points

        route = [] #List of CartesianPoints


        if mission.direction == HORIZONTAL_DIRECTION:
            if mission.movement == UP_MOVEMENT:
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
            if mission.direction == UP_MOVEMENT:
                A = 0
                B = 3
                C = 2
                D = 1

            else:
                A = 2
                B = 1
                C = 0
                D = 3


        route.append(area.hypotenuse)

        # Generalizing
        r_bar = points[C].minus(points[B]).divide(mission.turn_qty - 1)
        l_bar = points[D].minus(points[A]).divide(mission.turn_qty - 1)

        route.append(points[A])
        route.append(points[B])


        for i in range(mission.turn_qty):
            if i%2 == 0:
                route.append(points[A].sumproduct(i, l_bar))
                route.append(points[B].sumproduct(i, r_bar))

            else:
                route.append(points[B].sumproduct(i, r_bar))
                route.append(points[A].sumproduct(i, l_bar))


        route.append(home)

        return Route(route, mission)


    def calc_route(): #throws FileNotFoundException, IOException
        route = calc_complete_route()
        mission = self.mission

        print("-------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------")
        print("Quantidade de voltas: " + mission.turn_qty)
        print("Quantidade de WayPoints: " + len(route.route))
        print("Comprimento da volta: " + mission.turn_lenght)
        print("Largura da volta: " + mission.turn_width)
        print("Width da foto: " + mission.width)
        print("Height da foto: " + mission.height)
        print("Hipotenusa: " + mission.area.hypotenuse)
        print("Comprimento da base: " + mission.area.base_lenght)
        print("Comprimento total da rota: " + route.route_length + "metros")
        print("-------------------------------------------------------------------------------")
        print("P0: " + mission.area.point[0])
        print("P1: " + mission.area.point[1])
        print("P2: " + mission.area.point[2])
        print("P3: " + mission.area.point[3])
        print("Quantidade de Fotos: " + route.picture_qty)
        print("Velocity Shutter: " + mission.velocity_shutter)
        print("Velocity Cruiser: " + mission.velocity_cruiser)
        print("Flight Time: " + route.flight_duration / 60)
        print("Pictures Per Second: " + route.picture_per_second)
        print("Pictures Precision: " + mission.picture_precision)
        print("Precisão em milimetros: " + calc_GSD(mission))
        print("-------------------------------------------------------------------------------")

        route = [] #List of CartesianPoints

        if mission.drone.min_battery < route.flight_duration:
            mission_qty = math.ceil((route.flight_duration / 60) / mission.drone.min_battery) # ToDo: verificar essa função da math

            index = split_index(route.route, mission_qty) # ToDo: verificar essa função

            index.addFirst(1) # ToDo: verificar função
            index.addLast(len(route.route) - 2) # ToDo: verificar função

            for m in range(mission_qty):
                sub_route = build_sub_route(route.route, index.get(m), index.get(m + 1))
                sub_route.addFirst(mission.area.hypotenuse) # ToDo: verificar função
                sub_route.addLast(mission.area.hypotenuse) # ToDo: verificar função

                sub = Route(sub_route, mission)

                print("----------------------------------------------(SubRoute " + (m+1) + ")---------------------------------------------------")
                print("Número de WayPoints: " + sub_route.size())
                print("Comprimento da rota: " + sub.route_length)
                print("Número de Fotos " + sub.picture_qty)
                print("Flight Time " + sub.flight_duration / 60)
                print("Pictures Per Second " + sub.picture_per_second)
                #print(sub.geoRoute.stream().map(e -> e.toString()).reduce(String::concat).get()) # ToDo: verificar função

                routes.append(sub)

            else:
                routes.append(route)


            save_kml(routes, mission)
            save_litchi(routes, mission)


    def save_litchi(routes, mission): #throws FileNotFoundException
        count = 1

        for route in routes:
            with open(path + 'route' + count + '.csv', 'r') as file: # ToDo: definir path 
                file.write("latitude,longitude,altitude(m),heading(deg),curvesize(m),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(m),poi_altitudemode,photo_timeinterval")

                for geo_point in route.geo_route:
                    file.write(geo_point.latitude + ',' 
                        + geo_point.latitude + ','
                        + calc_heading(mission.area.point[0], mission.area.point[1]) + ','
                        + "0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1"
                        )


    def save_kml_point(file, point, name):

        file.write("<Placemark>")
        file.write("<name>%s</name>\n", name)
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
        file.write("<coordinates>%1.15f,%1.15f,%1.15f</coordinates>\n", point.longitude, point.latitude, point.height)
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

        with open(path + 'mission.kml', 'r') as file: # ToDo: definir path 

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
                route.save_kml(file, "route" + count)
                count += 1 
            
            save_kml_point(file, mission.area.home, "H")

            count = 0
            for point in mission.area.points:
                save_kml_point(file, point, "P"+ count)
                count += 1

            file.write("</Folder>")
            file.write("</Document>")
            file.write("</kml>")


    def calc_heading_cartesian(c1, c2):
        heading = 360 - math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi() # ToDo: verificar

        heading = heading % 360 #if heading>360 else heading # ToDo: simplificar com expressão de cima

        print("%5.2f %5.2f %5.2f\n", c1.x, c1.y, c1.z)
        print("%5.2f %5.2f %5.2f\n", c2.x, c2.y, c2.z)
        print("dx = %5.2f \n", (c2.x - c1.x))
        print("dy = %5.2f \n", (c2.y - c1.y))
        print("dy/dx = %5.2f \n", (c2.y - c1.y) / (c2.x - c1.x))
        print("dy/dx = %5.2f \n", math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi()) # ToDo: verificar

        print(heading)
        return heading


    def calc_heading_geo(p1, p2, home):
        c1 = to_cartesian(p1, home)
        c2 = to_cartesian(p2, home)

        heading = math.atan2((c2.y - c1.y), (c2.x - c1.x)) * 180 / math.pi() + 90 # ToDo: verificar
        return heading


    def calc_route_length(route):
        total_length = 0
        current = route.getFirst() # ToDo: verificar

        for element in route:
            total_length += element.minus(current).norm()
            current = element

        return total_length


    def build_sub_route(route, first_i, last_i):
        res = []

        for i in range(first_i, last_i):
            res.append(route.get(i))

        return res


    def split_index(route, mission_qty):
        size = math.floor(len(route) / mission_qty)

        res = []

        for m in range(mission_qty):
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
            final_route.append(to_geo_point(element, home))

        return final_route


    def to_geo_point(cartesian_point, home):
        longitude_x = calc_longitude_x(home.latitude, home.longitude, cartesian_point.x)
        latitude_y = calc_latitude_y(home.latitude, cartesian_point.y)

        return GeoPoint(longitude_x, latitude_y, cartesian_point.z)


    def to_cartesian(geo_point, home):
        x = calc_x(geo_point.longitude, home.longitude, home.latitude)
        y = calc_y(geo_point.latitude, home.latitude)

        return CartesianPoint(x, y, geo_point.height)


    def calc_y(lat, lat_):
        return (lat - lat_) * (10000000.0 / 90)


    def calc_x(longi, longi_, lat_):
        pi = math.pi()
        return (longi - longi_) * (6400000.0 * (math.cos(lat_ * pi / 180) * 2 * pi / 360)) # ToDo: verificar math


    def calc_latitude_y(lat_, y):
        return ((y * 90) / 10000000.0) + lat_


    def calc_longitude_x(lat_, longi_, x):
        return ((x * 90) / (10008000 * math.cos(lat_ * math.pi() / 180))) + long_


    def photo_lenght_on_ground(picture_distance, camera_opening):
        return 2 * picture_distance * Math.tan((camera_opening / 2) * math.pi() / 180)


    def calc_denescala(mission): # ToDo: renomear
        return mission.picture_distance / (mission.camera.focus_distance * (10**-3))


    def calc_sensor_x(mission): # ToDo: simplificar
        return mission.camera.sensor['x'] / mission.camera.resolution['w']

    def calc_sensor_y(mission):
        return mission.camera.sensor['y'] / mission.camera.resolution['h']

    def calc_tam(mission):
        a = calc_sensor_x(mission)
        b = calc_sensor_y(mission)

        return math.min(a, b) # ToDo: verificar

    def calc_GSD(mission):
        denescala = calc_denescala(mission)
        tam = calc_tam(mission)
        print(denescala + "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        return denescala * tam






























