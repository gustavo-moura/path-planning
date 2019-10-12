from collections import namedtuple
from utils import controller

import math

class Area():

    def __init__(self, geo_home, geo_points):
        self.geo_home = geo_home
        self.geo_points = geo_points
        self.home = controller.to_cartesian(geo_home, geo_home) # ToDo: ???
        self.points = controller.to_cartesians(geo_points, geo_home) # points = [p1, p2, p3, p4] # point order not verified # ToDo: verify order
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


    def get_edges(self):
        edges = []

        edge = namedtuple('edge', 'A B')

        qtd = len(self.points)

        for i in range(qtd-1):
            e = edge(self.points[i], self.points[i+1])
            edges.append(e)

        e = edge(self.points[qtd-1], self.points[0])
        edges.append(e)

        return edges



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


    def minus(self, other):
        # Distance between two points, in meters
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z

        return CartesianPoint(x, y, z)


    def plus(self, other):
        # Sum between two cartesian points
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z

        return CartesianPoint(x, y, z)


    def divide(self, number):
        # Divide the cartesian point by a number
        '''
        P3 = P1 / number Divide um vetor grande em partes pequenas para a
        formação da rota.
        '''
        x = self.x / number
        y = self.y / number
        z = self.z / number

        return CartesianPoint(x, y, z)

    
    def sumproduct(self, coef, other):
        '''
        Adiciona no ponto atual com um outro ponto multiplicado por um
         * coeficiente. P3 = P1 + coef * P2 P3 é o resultado a ser retornado P1 é o
         * objeto atual ao qual foi chamado a função P2 é o objeto passado como
         * parâmetro.
        '''
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


    def calc_turn_qty(self, hypotenuse, width, sobrePosicao):
        # Calculate the turns quantity
        return (0.8 + hypotenuse / (width * (1 - sobrePosicao))) + 1


    def photo_length_on_ground(self, picture_distance, camera_opening):
        return 2 * picture_distance * math.tan((camera_opening / 2) * math.pi / 180)



class Route():

    def __init__(self, route, mission):
        self.route = route
        self.geo_route = Controller.transform_geo_points(route, mission.area.geo_home) #ToDo: checar essa função
        self.route_length = self.calc_route_length()

        if mission.direction == mission.HORIZONTAL_DIRECTION:
            measure = mission.width
        else:
            measure = mission.height

        self.picture_qty = round(self.route_length / (measure * (1 - mission.sobrePosicao)))   
        self.flight_duration = (self.route_length / mission.velocity_cruiser)
        self.picture_per_second = self.picture_qty / self.flight_duration
            

    def calc_route_length(self):
        route = self.route
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

