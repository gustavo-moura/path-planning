import math
import random

import matplotlib.pyplot as plt

from algorithms.genetic_algorithm import objectivefunction as of

QUIETUS = 1000 # Quantity of generations until the species extinction
SUBJECT_QTY = 100 # Quantity of subjects in the population
GENE_QTY = 5 # Horizonte de planejamento # T
path = ''
# https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python

class Subject():

    # fitness = float

    # gene_qty

    # codificação - u
    # dna = [[a, e], ...]
    #     a = float: aceleração
    #     e = float: variação angular

        # gene = [a, e]

    # decodificação - x
    # x = [(px, py, v, al), ...]
    #     x = : Posição do VANT no eixo x 
    #     y = : Posição do VANT no eixo y
    #     v = : Velocidade do VANT na horizontal
    #     a = : ângulo (direção) do VANT na horizontal

    # mutation_rate = float

    def __init__(self, gene_qty=GENE_QTY, mutation_rate=0):
        self.gene_qty = gene_qty
        self.dna = [self.random_gene() for i in range(self.gene_qty)]
        self.mutation_rate = mutation_rate


    def cross(self, parent):
        dna1 = self.dna
        dna2 = parent.dna

        # print("DNA", type(dna1[0]), type(dna2[0]))

        offspring = Subject()

        dna = [self.crossover_function(gene1, gene2) for gene1, gene2 in zip(dna1, dna2)]

        offspring.dna = dna

        return offspring
        

    def crossover_function(self, gene1, gene2):
        # Crossover média
        a = (gene1[0] + gene2[0])/2
        e = (gene1[1] + gene2[1])/2
        
        return [a, e]


    def mutate(self):
        # Mutação Creep

        for gene in self.dna:
            gene[0] += self.mutation_expression()
            gene[1] += self.mutation_expression()

        return self

    def mutation_expression(self):
        return (self.mutation_rate * random.choice([1, -1]))


    def random_gene(self):
        # Inicialização Aleatoria

        a = random.uniform(0.5, 10)
        e = random.uniform(0.5, 2*math.pi)
        return [a, e]


    def get_omega(self):
        #       ( px  ,  py  )
        return [(xt[0], xt[1]) for xt in self.x]


    def transitar(self, mapa):
        self.x = []
        i = 0
        self.x.append((mapa.origem.x, mapa.origem.y, 0, 0))
        for gene in self.dna:
            self.x.append(of.transitar_(self, i))
            i += 1



class GeneticAlgorithm():

    # Subject = class
    # population = [Subject, ...]
    # best = Subject
    # ancestry = [Subject, ...]
    # epoch = int
    # verbose = bool
    # mapa = Mapa

    def __init__(self, Subject, mapa, verbose=False, plot=False):
        self.Subject = Subject
        self.mapa = mapa
        self.verbose = verbose
        self.plot = plot

        self.ancestry = []


    # ----------------- Class interactions




    # ----------------- Algorithm parts

    def run(self, size=SUBJECT_QTY, _quietus=QUIETUS):

        # 1 Initialization
        self.population = self.generate_population(size)

        self.epoch = 0
        while self.epoch < _quietus: # ToDo: alterar

            # 2 Fitness assignment
            self.best = self.evaluate()

            # 3 Selection
            #self.best = max(self.population.fitness) # ToDo: verificar
            self.ancestry.append(self.best) # Never kill the best subject

            # 4 Crossover
            new_population = self.crossover(self.population)

            # 5 Mutation
            mutated_new_population = self.mutate(new_population)

            # 6 Extintion
            mutated_new_population.pop()
            self.population = mutated_new_population + [self.best]

            self.epoch += 1

            if self.verbose:
                print("Epoch: {}; Best_fitness: {}".format(self.epoch, self.best.fitness))
        if self.plot:
            self.plotar(self.ancestry)

    def generate_population(self, size):
        return [self.Subject() for i in range(size)]


    def evaluate(self):
        best = self.population[0]

        for subject in self.population:
            subject.transitar(self.mapa)

            fit = of.objective_function(subject, self.mapa)
            subject.fitness = fit

            if subject.fitness < best.fitness:
                # print("new best", subject.fitness, best.fitness)
                best = subject

        return best


    def crossover(self, population):
        return [parent.cross(self.best) for parent in population]


    def mutate(self, population):
        return [subject.mutate() for subject in population]



    def plotar(self, ancestry):
        ancestry_fitness = [subject.fitness for subject in ancestry]

        plt.plot(ancestry_fitness)
        plt.xlabel('epoch')
        plt.ylabel('fitness')
        plt.show()


    # Format for MAVROS
    def save_litchi(self, routes):
        count = 1
        path = ''

        for route in routes:
            with open(path + 'AG_mavros' + str(count) + '.wp', 'w+') as file: # ToDo: definir path 
                #file.write("latitude,longitude,altitude(m),heading(deg),curvesize(m),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(m),poi_altitudemode,photo_timeinterval\n")
                current_waypoint = 1

                file.write('QGC WPL 120\n') # Determines the file version

                i = 0

                for geo_point in route:
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


    def route_save_kml(self, file, name, geo_route): # ToDo: corrigir
        file.write("<Placemark>")
        file.write("<name>" + name + "</name>")
        file.write("<styleUrl>#m_ylw-pushpin0000</styleUrl>")
        file.write("<LineString>")
        file.write("<tessellate>1</tessellate>")
        file.write("<altitudeMode>relativeToGround</altitudeMode>")
        file.write("<coordinates>")
        #print('##############################################################################\n')
        for waypoint in geo_route:
            file.write("{},{},{}\n".format(waypoint.longitude, waypoint.latitude, waypoint.height))

        #print('##############################################################################\n')
        #file.write(this.geoRoute.stream().map(e -> e.toString()).reduce(String::concat).get()) # ToDo: checar e corrigir
        file.write("</coordinates>")
        file.write("</LineString>")
        file.write("</Placemark>")


    def save_kml_point(self, file, point, name):
        # print("\n\n")
        # print(type(point))
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
        
        # if type(point) == type([]):
        #     file.write("<coordinates>{},{},{}</coordinates>".format(point[0], point[1], point[2]))
        # else:
        file.write("<coordinates>{},{},{}</coordinates>".format(point.longitude, point.latitude, point.height))
        file.write("</Point>")
        file.write("</Placemark>")

    def save_kml(self, routes, geo_home, geo_points): #throws FileNotFoundException

        with open(path + 'mission.kml', 'w+') as file: 

            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            file.write("<kml>")
            file.write("<Document>")
            file.write("<name>AG_C2.kml</name>")
            file.write("<name>AG_C2.kml</name>")
            file.write("<Folder>")
            file.write("<name>AG_C2</name>")
            file.write("<open>1</open>")
           
            count = 0
            for route in routes:
                self.route_save_kml(file, "route" + str(count), route)
                count += 1 
            
            self.save_kml_point(file, geo_home, "H")

            count = 0
            for geo_point in geo_points:
                self.save_kml_point(file, geo_point, "P"+ str(count))
                count += 1

            file.write("</Folder>")
            file.write("</Document>")
            file.write("</kml>")