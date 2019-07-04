# todo: change filename to pathplanning.py


class Area():

    def __init__(self, geo_home=geo_home, geo_points=geo_points):

        self.geo_home = geo_home
        self.geo_points = geo_points
        self.home = cartesian(geo_home)
        self.points = cartesian(geo_points) # points = [p1, p2, p3, p4]
        self.hypotenuse = calc_hypotenuse(points)
        self.base_lenght = calc_base_lenght(points)


    def calc_hypotenuse(self, point):
        pass
    
    def calc_base_lenght(self, point):
        pass
    '''
    private static double calcHipotenusa(CartesianPoint p1, CartesianPoint p2, CartesianPoint p3, CartesianPoint p4) {
        CartesianPoint h1 = p4.minus(p1);
        CartesianPoint h2 = p3.minus(p2);
        return Math.max(h1.norm(), h2.norm());
    }

    private double calcComprimentoBase(CartesianPoint p1, CartesianPoint p2, CartesianPoint p3, CartesianPoint p4) {
        CartesianPoint h1 = p4.minus(p3);
        CartesianPoint h2 = p1.minus(p2);
        return Math.max(h1.norm(), h2.norm());
    }
    '''


class Camera():

    def __init__(self, open_angle=open_angle, resolution=resolution, 
        max_zoom=max_zoom, shutter_time=shutter_time, mega_pixel=mega_pixel,
        trigger=trigger, weight=weight, sensor=sensor, 
        focus_distance=focus_distance):

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

    self.id = None
    self.id_count = 0

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
    P3 = P1 / number; Divide um vetor grande em partes pequenas para a
    formação da rota.
    '''
    def divide(self, number):
        x = self.x / number
        y = self.y / number
        z = self.z / number

        return CartesianPoint(x, y, z)

    '''
    Adiciona no ponto atual com um outro ponto multiplicado por um
     * coeficiente. P3 = P1 + coef * P2 P3 é o resultado a ser retornado; P1 é o
     * objeto atual ao qual foi chamado a função; P2 é o objeto passado como
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

    def __init__(weight=weight, min_battery=min_battery, 
        max_battery=max_battery, max_velocity=max_velocity, 
        efficient_velocity=efficient_velocity):

        self.weight = weight
        self.min_battery = min_battery
        self.max_battery = max_battery
        self.max_velocity = max_velocity
        self.efficient_velocity = efficient_velocity


    
class GeoPoint():

    def __init__(longitude=longitude, latitude=latitude, height=height):
        
        self.longitude = longitude
        self.latitude = latitude
        self.height = height



class Mission():
    self.HORIZONTAL_DIRECTION = 1
    self.VERTICAL_DIRECTION = 2
    self.UP_MOVEMENT = 3
    self.DOWN_MOVEMENT = 4

    def __init__(direction=direction, movement=movement, drone=drone, 
        camera=camera, area=area, SD_card=SD_card, 
        picture_distance=picture_distance, zoom=zoom, 
        sobrePosicao=sobrePosicao, blur_factor=blur_factor):

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


        self.width = photo_lenght_on_ground(picture_distance, camera.open_angle['w'])
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
            self.flight_lenght = (route_length / mission.velocity_cruiser)
            self.picture_per_second = picture_qty / flight_lenght


    def saveKml(PrintStream out, String name) { # ToDo: corrigir
        print("<Placemark>")
        print("<name>" + name + "</name>")
        print("<styleUrl>#m_ylw-pushpin0000</styleUrl>")
        print("<LineString>")
        print("<tessellate>1</tessellate>")
        print("<altitudeMode>relativeToGround</altitudeMode>")
        print("<coordinates>")
        #print(this.geoRoute.stream().map(e -> e.toString()).reduce(String::concat).get()) # ToDo: checar e corrigir
        print("</coordinates>")
        print("</LineString>")
        print("</Placemark>")






   