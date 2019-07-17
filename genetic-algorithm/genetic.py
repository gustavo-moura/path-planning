import math

class Subject():

    # fitness = int

    # dna = [(a, e), ...]
    #     a = float: aceleração
    #     e = float: variação angular

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
            subject.fitness = self.objective_function()


    def crossover(self):
        return [parent.cross(self.best) for parent in self.population]


    def mutate(self):
        return [subject.mutate() for subject in self.population]


    def objective_function():
        fitness = f_pouso_b + f_pouso_p + f_pouso_voo_n + f_curvas + f_dist + f_viol + f_bat



    def f_pouso_b():
        # Define recompensa em caso de pouso em regiões bonificadoras.
        Cb = custo de pousar no conjunto bonificador

        custo * somatoria da probabilidade de pousar em cada uma das regiões bonificadoras


    def f_pouso_p(): 
        # Define punição em caso de pouso em regiões penalizadoras.

    def f_pouso_voo_n():
        # Penaliza o pouso ou voo da aeronave sobre regiões não navegáveis.
        ???

        
    def f_curvas():
        # Prioriza rotas que evitem fazer curvas desnecessárias.

    def f_dist():
        # Dá mais chance a rotas com menores distâncias das regiões bonificadoras.

    def f_viol():
        # Se a aeronave tem velocidade final maior do que o seu valor mínimo, não ocorre de fato
        # um pouso. Dessa maneira, a Equação (f_viol) evita rotas em que o VANT não consegue pousar,
        # mesmo que atinja uma região bonificadora.

    def f_bat():
        # Se houver um problema na bateria, a Equação (f_bat) é adicionada à função de fitness. O
        # objetivo é reduzir o tempo de voo, assim a aeronave buscará regiões para pouso mais próximas
        # de sua localização no momento onde ocorreu a pane.





