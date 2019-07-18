import math
import objectivefunction as of

class Subject():

    # fitness = int

    # codificação - u
    # dna = [(a, e), ...]
    #     a = float: aceleração
    #     e = float: variação angular

    # decodificação - x
    # x = [(px, py, v, al), ...]
    #     px = : Posição do VANT no eixo x 
    #     py = : Posição do VANT no eixo y
    #     v  = : Velocidade do VANT na horizontal
    #     al = : ângulo (direção) do VANT na horizontal

    # mutation_rate = float

    def __init__(planning_horizon=60, mutation_rate=0.1):
        self.dna = [self.random_gene() for i in range(self.planning_horizon)]
        self.mutation_rate = mutation_rate


    def cross(self, parent):
        dna1 = self.gene
        dna2 = parent.gene

        offspring = Subject()

        dna = [crossover_function(gene1, gene2) for gene1, gene2 in zip(dna1, dna2)]

        offspring.dna = dna

        return offspring
        

    def crossover_function(gene1, gene2):
        # Crossover média

        return (gene1 + gene2) / 2


    def mutate(self):
        # Mutação Creep

        for gene in self.dna:
            gene[0] += mutation_rate
            gene[1] += mutation_rate


    def random_gene():
        # Inicialização Aleatoria

        a = random.uniform(0.5, 10)
        e = random.uniform(0.5, 2*math.pi)
        return (a, e)


    def get_omega():
        #       ( px  ,  py  )
        return [(xt[0], xt[1]) for xt in x]



class GeneticAgorithm():

    # Subject = class
    # population = [Subject, ...]
    # best = Subject
    # ancestry = [Subject, ...]
    # epoch = int

    def __init__(Subject):
        self.Subject = Subject
        self.ancestry = []


    def run(self):

        # 1 Initialization
        self.population = self.generate_population(size)

        while not stop(???): # ToDo

            # 2 Fitness assignment
            self.evaluate(population)

            # 3 Selection
            self.best = max(population.fitness) # ToDo: verificar
            self.ancestry.append(self.best) # Never kill the best subject

            # 4 Crossover
            new_population = crossover(population)

            # 5 Mutation
            mutated_new_population = mutate()

            # 6 Extintion
            self.population = mutated_new_population

            self.epoch += 1



    def generate_population(self, size):
        return [self.Subject() for i in range(size)]


    def evaluate(self, population):
        for subject in self.population:
            subject.fitness = of.objective_function()


    def crossover(self):
        return [parent.cross(self.best) for parent in self.population]


    def mutate(self):
        return [subject.mutate() for subject in self.population]




