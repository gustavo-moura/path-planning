import os
import sys
nb_dir = os.path.split(os.getcwd())[0]
if nb_dir not in sys.path:
    sys.path.append(nb_dir)


import file_manipulation




class Planning():

    def __init__(self, mission):
        self.mission = mission


    '''
    Transforma os pontos geográficos da missão em pontos cartesianos em
    metros para efetuar o cálculo da rota. Após isso, é calculado os pontos
    da rota que o drone irá fazer com base no número de voltas para fazer o
    mapeamento completo da área. Então é transformado de pontos cartesianos
    da rota em metros para pontos geográficos e adionados na lista final.
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
        # ToDo: add verbose
        route = self.calc_complete_route()
        mission = self.mission

       	self.print_route(route, mission)

        routes = [] #List of CartesianPoints

        if mission.drone.min_battery < route.flight_duration:
            mission_qty = math.ceil((route.flight_duration / 60) / mission.drone.min_battery) # ToDo: verificar essa função da math

            index = self.split_index(route.route, mission_qty) # ToDo: verificar essa função

            index.insert(0, 1) # addFirst(1)
            index.insert(len(index), len(route.route)-2) # addLast(len(route.route) - 2)


            for m in range(mission_qty):
                sub_route = self.build_sub_route(route.route, index[m], index[m + 1])
                sub_route.insert(0, mission.area.home) # addFirst(mission.area.home)
                sub_route.insert(len(sub_route), mission.area.home) # addLast(mission.area.home)
                
                sub = Route(sub_route, mission)

                self.print_subroute(sub_route, sub)

                routes.append(sub)

            else:
                routes.append(route)

        self.routes = routes
        self.mission = mission


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



    def save(self, file_type, filename):
    	# ToDo: raise exceptions
    	if type(file_type) == type(list()):
    		print("Saving many files...")
    		for ftype in file_type:
    			self.save(ftype, filename)

    	else:
	    	if file_type == 'kml':
	    		fname = file_manipulation.save_kml(filename, routes, mission)
	        	print('Saved KML (.kml) file, named as "{}"'.format(fname))
	        
	        elif file_type == 'mavros':
	        	fname = file_manipulation.save_mavros(filename, routes, mission)
	        	print('Saved Mavros waypoints (.wp) file, named as "{}"'.format(fname))

	    return True


    def calc_denescala(self, mission): # ToDo: renomear
        return mission.picture_distance / (mission.camera.focus_distance * (10**-3))


    def calc_sensor_x(self, mission): # ToDo: simplificar
        return mission.camera.sensor[0] / mission.camera.resolution[1]

    def calc_sensor_y(self, mission):
        return mission.camera.sensor[1] / mission.camera.resolution[1]

    def calc_tam(self, mission):
        a = self.calc_sensor_x(mission)
        b = self.calc_sensor_y(mission)

        return min(a, b) # ToDo: verificar

    def calc_GSD(self, mission):
        denescala = self.calc_denescala(mission)
        tam = self.calc_tam(mission)
        #print(str(denescala) + "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        return denescala * tam


    def print_route(self, route, mission):
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
        print("Precisão em milimetros: " + str(self.calc_GSD(mission)))
        print("-------------------------------------------------------------------------------")


    def print_subroute(self, sub_route, sub):
    	print("----------------------------------------------(SubRoute ", m, ")---------------------------------------------------")
        print("Quantidade de WayPoints: ", len(sub_route))
        print("Comprimento da rota: ", sub.route_length)
        print("Quantidade de Fotos ", sub.picture_qty)
        print("Flight Time ", sub.flight_duration / 60)
        print("Pictures Per Second ", sub.picture_per_second)
        #print(sub.geoRoute.stream().map(e -> e.toString()).reduce(String::concat).get()) # ToDo: verificar função




