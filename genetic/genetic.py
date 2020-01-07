import collections
import random
import time
import copy

from math import cos, sin, sqrt, ceil

# from itertools import tee

from genetic.utils import pairwise, point_in_polygon, segment_in_polygon

# from genetic.utils import _distance_wp_area, _prob_collision

from genetic.data_definitions import CartesianPoint  # , Version

Gene = collections.namedtuple("Gene", "a e")
GeneDecoded = collections.namedtuple("GeneDecoded", "x y v al")


class Subject:
    def __init__(
        self,
        px0=10.0,
        py0=10.0,
        v0=0,
        al0=0,
        v_min=11.1,
        v_max=30.5,
        e_min=-3,
        e_max=3,
        a_min=-2.0,
        a_max=2.0,
        T=10,
        T_min=1,
        T_max=25,
        delta_T=1,
        m=743.0,
        mutation_prob=0.7,
        start_time=None,
        generation=None,
        id=-1,
        **kwargs
    ):
        # codificação - u
        # dna = [Gene, ...]
        #     Gene = [a, e]
        #         a = float: aceleração
        #         e = float: variação angular

        # decodificação - x
        # dna_decoded = [GeneDecoded, ...]
        #     GeneDecoded = (x, y, v, al)
        #         x  = : Posição do VANT no eixo x (aka px)
        #         y  = : Posição do VANT no eixo y (aka py)
        #         v  = : Velocidade do VANT na horizontal
        #         al = : ângulo (direção) do VANT na horizontal

        # VANT
        # px0   int : Posição inicial no eixo x (m)
        # py0   int : Posição inicial no eixo y (m)
        # v0    int : Velocidade Inicial (m/s)
        # al0   int : Ângulo inicial (graus)
        self.gene_decoded_0 = GeneDecoded(
            px0, py0, v0, al0
        )  # GeneDecoded : objeto contendo o gene decodificado de posição 0
        self.v_min = v_min  # float : Velocidade máxima (m/s)
        self.v_max = v_max  # float : Velocidade mínima (m/s)
        self.e_min = e_min  # int   : Velocidade angular mínima (graus/s)
        self.e_max = e_max  # int   : Velocidade angular máxima (graus/s)
        self.a_min = a_min  # float : Aceleração mínima (m/s**2)
        self.a_max = a_max  # float : Aceleração máxima (m/s**2)

        # Modelo
        self.T_min = T_min  # int : Valor mínimo para o horizonte de planejamento
        self.T_max = T_max  # int : Valor máximo para o horizonte de planejamento
        self.delta_T = delta_T  # int : Discretização do tempo (s) Tempo que leva de um waypoint até o outro
        self.m = m  # float : Massa do VANT (!=0) (gramas)

        # Parametros do indivíduo
        self.mutation_prob = (
            mutation_prob  # float : Probabilidade de ocorrer uma mutação no dna (%)
        )
        self.fitness = None  # float : Fitness do indivíduo
        # self.birth_time    = None          # time  : Hora que o indivíduo é criado
        self.dna = None  # list  : Conjunto de genes formando o DNA ([Gene, ...])
        self.dna_decoded = None  # list  : DNA decodificado ([GeneDecoded, ...])
        # spawn_mode="random",
        # self.spawn_mode = spawn_mode  # str   : Tipo de incialização do DNA {'random'}
        self.start_time = start_time  # time  : a hora em que o genético começou a rodar
        self.generation = generation
        self.id = id
        self.parents = []

        # assert version, 'Algorithm version must be informed!\nEx: Version("alpha","RC")'
        # if version.major == "alpha":  # Sem otimização em T
        #     self.T = T
        #     self.mutation_choices = [self._mutation_creep, self._mutation_change]
        # elif version.major == "beta":  # Com otimização em T
        #     self.T = random.randint(
        #         T_min, T_max
        #     )  # int : Horizonte de planejamento (quantidade de waypoints)
        #     self.mutation_choices = [
        #         self._mutation_remove,
        #         self._mutation_insert,
        #         self._mutation_creep,
        #         self._mutation_change,
        #     ]

        self.T = random.randint(
            T_min, T_max
        )  # int : Horizonte de planejamento (quantidade de waypoints)
        # self.mutation_choices = [
        #     self._mutation_remove,
        #     self._mutation_insert,
        #     self._mutation_creep,
        #     self._mutation_change,
        # ]

        # self.spawn(mode=spawn_mode)
        self.spawn()

    def __repr__(self):
        return f'({self.id}, {self.parents})'

    # ---

    def to_dict(self):
        return {
            "id": self.id,
            "generation": self.generation,
            "parents": self.parents,
            "fitness": self.fitness,
            "fitness_trace": self.fitness_trace,
            "birth_time": self.birth_time,
            "route": self.get_route(),
        }

    # ---

    def set_fitness(self, fitness, fitness_trace):
        self.fitness = fitness
        self.fitness_trace = fitness_trace

    def set_generation(self, generation):
        self.generation = generation

    def set_id(self, id):
        self.id = id

    def set_parents(self, parent1, parent2):
        self.parents.append(parent1.id)
        self.parents.append(parent2.id)

    # ---

    def spawn(self):
        # def spawn(self, mode):
        #     self.dna = [self._build_gene(mode) for _ in range(self.T)]
        self.dna = [self._build_gene() for _ in range(self.T)]

    def _build_gene(self):
        # def _build_gene(self, mode="random"):
        #     # Inicialização aleatória gera valores com distribuição uniforme
        #     if mode == "random":
        #         a = random.uniform(self.a_min, self.a_max)
        #         e = random.uniform(self.e_min, self.e_max)
        # Inicialização aleatória gera valores com distribuição uniforme
        a = random.uniform(self.a_min, self.a_max)
        e = random.uniform(self.e_min, self.e_max)

        return Gene(a, e)

    # ---

    def decode(self):
        # self.dna_decoded = [self._decode_gene() for i in range(len(self.dna))]
        self.dna_decoded = (
            self._decode_gene()
        )  # TODO: Organizar, voltar como era a linha de cima. Fazer função abaixo só computar o gene
        self.birth_time = time.time() - self.start_time

    def _decode_gene(self):
        dna = self.dna

        # parametros
        delta_T = self.delta_T
        # m = self.m

        dna_decoded = []
        dna_decoded.append(self.gene_decoded_0)

        for i in range(0, len(dna)):
            # dna
            a = dna[i].a
            e = dna[i].e

            # dna decodificado
            px = dna_decoded[i].x
            py = dna_decoded[i].y
            v = dna_decoded[i].v
            al = dna_decoded[i].al

            # F = self.__F(v)

            # Equações descritas em (Arantes 2016) - adaptações por Claudio (jan/20)
            _px = px + (v * cos(al) * delta_T) + (a * cos(al) * ((delta_T ** 2) / 2))
            _py = py + (v * sin(al) * delta_T) + (a * sin(al) * ((delta_T ** 2) / 2))
            _v = v + (a * delta_T)  # - ((F / m) * delta_T)
            _al = al + (e * delta_T)

            dna_decoded.append(GeneDecoded(_px, _py, _v, _al))

        return dna_decoded

    def __F(self, v):
        # Equação do Arrasto
        # Disponível em https://pt.wikipedia.org/wiki/Equa%C3%A7%C3%A3o_do_arrasto
        # Versão utilizada ((Arantes, 2016) equação 3.5)

        Cd = 0.8  # float : Coeficiente de arrasto, específico para cada aeronave
        #         (considerado Angled Cube) obtido de https://pt.wikipedia.org/wiki/Coeficiente_de_resist%C3%AAncia_aerodin%C3%A2mica
        rho = 1.225  # float : Massa específica do fuído (aka densidade) (k/m**3)
        #         (a 15 graus Celsius) Valor de rho obtido de https://pt.m.wikipedia.org/wiki/Densidade_do_ar
        A = 1.0  # float : Área de referência # TODO: o que é isso?
        # v = v       # float : Velocidade do Vant no instante t (fornecido como parâmetro da função)

        F = 0.5 * Cd * rho * A * (v ** 2)

        return F

    # ---

    def crossover(self, parent2, Specie, **kwargs):
        dna = random.choice([self._OX, self._BLX_Alpha])(self.dna, parent2.dna)
        dna = self._complete(dna, self.dna, parent2.dna)
        child = self.generate(dna, Specie, **kwargs)
        return child

    def _OX(self, dna1, dna2):
        dna = []
        for gene1, gene2 in zip(dna1, dna2):
            dna.append(random.choice([gene1, gene2]))
        return dna

    def _BLX_Alpha(self, dna1, dna2):
        dna = []
        for gene1, gene2 in zip(dna1, dna2):
            a = self.__BLX_ALpha_select_gene(gene1.a, gene2.a)
            e = self.__BLX_ALpha_select_gene(gene1.e, gene2.e)
            if a > self.a_max:
                a = self.a_max
            elif a < self.a_min:
                a = self.a_min

            if e > self.e_max:
                e = self.e_max
            elif e < self.e_min:
                e = self.e_min

            gene = Gene(a, e)
            dna.append(gene)

        return dna

    def __BLX_ALpha_select_gene(self, x, y):
        # x - Gene : gene do pai 1
        # y - Gene : gene do pai 2
        alpha = random.uniform(0, 1)
        d = abs(x - y)
        u = random.uniform(min(x, y) - alpha * d, max(x, y) + alpha * d)
        return u

    def _complete(self, dna, dna1, dna2):
        # Adiciona os genes restantes da diferença de tamanho entre os dois DNAs

        if len(dna1) > len(dna2):
            bigger = dna1
            smaller = dna2
        else:
            bigger = dna2
            smaller = dna1

        for i in range(len(smaller) - 1, len(bigger) - 1):
            if random.random() < 0.5:
                dna.append(bigger[i])

        return dna

    def generate(self, dna, Specie, **kwargs):
        # Cria um filho com os mesmos parametros do pai, mas com um dna fornecido
        # child = copy.deepcopy(self)
        child = Specie(
            start_time=self.start_time,
            **kwargs
        )
        child.dna = dna
        child.decode()
        return child

    # ---

    def mutation(self, mutation_prob=None):
        mutation_prob = (
            self.mutation_prob if not mutation_prob else mutation_prob
        )  # 0.7

        # Tem uma probabilidade mutation_prob de mutar o gene ou não
        if random.random() < mutation_prob:
            # Seleciona aleatoriamente uma das formas de mutação
            # new_dna = random.choice(self.mutation_choices)(self.dna)
            new_dna = random.choice(
                [
                    self._mutation_remove,
                    self._mutation_insert,
                    self._mutation_creep,
                    self._mutation_change,
                ]
            )(self.dna)

            if new_dna:
                self.dna = new_dna
                self.decode()

            return True
        return False

    def _mutation_change(self, dna):
        # Reinicia um gene aleatoriamente
        new_dna = []
        for gene in dna:
            if random.random() < 0.5:
                # new_dna.append(self._build_gene("random"))
                new_dna.append(self._build_gene())
            else:
                new_dna.append(gene)

        return new_dna

    def _mutation_remove(self, dna):
        # Remove UM gene aleatório do DNA
        if len(dna) > self.T_min:
            i = random.randint(0, len(dna) - 1)
            dna.pop(i)
            return dna
        return None

    def _mutation_insert(self, dna):
        # Insere UM gene aleatório no DNA em uma posição aleatória
        if len(dna) < self.T_max:
            i = random.randint(0, len(dna) - 1)
            gene = self._build_gene()
            dna.insert(i, gene)
            return dna
        return None

    def _mutation_creep(self, dna):
        # Muta em um pequeno valor aleatorio todos os genes
        new_dna = []
        for gene in dna:
            a = self.__mute(gene.a, self.a_min, self.a_max)
            e = self.__mute(gene.e, self.e_min, self.e_max)

            # TODO2: otimizar
            new_gene = Gene(a, e)
            new_dna.append(new_gene)

        return new_dna

    def __mute(self, val, min_val, max_val):
        mutation_rate = random.uniform(0, max_val * 0.5)
        s = random.choice([1, -1])
        val = val * (1 + (mutation_rate * s))

        # Checa se não estoura os limites
        if val > max_val:
            val = max_val
        elif val < min_val:
            val = min_val
        # val = max(val, min_val)
        # val = min(val, max_val)

        return val

    # ---

    def get_route(self):
        return [[gene.x, gene.y] for gene in self.dna_decoded]


class Genetic:
    def __init__(
        self,
        Specie,
        mapa,
        taxa_cross=5,
        population_size=10,
        C_d=1000,
        C_obs=10000,
        C_con=500,
        C_cur=100,
        C_t=10,
        C_dist=1,
        max_exec_time=1,
        min_precision=1.0,
        k_tournament=2,
        gps_imprecision=1,
        big_delta=1,
        **kwargs
    ):
        # Modelo
        self.Specie = Specie  # objeto : Definição da classe (não a instância)
        self.mapa = mapa  # Mapa   : Mapa com as características da missão

        # Parâmetros
        self.taxa_cross = taxa_cross  # float : Taxa de ocorrencia do crossover [0,1]
        self.population_size = (
            population_size  # int   : Quantidade máxima de indivíduos na população
        )
        self.C_d = C_d  # int   : Custo associado ao fitness de destino
        self.C_obs = C_obs  # int   : Custo associado ao fitness de obstáculos
        self.C_con = (
            C_con  # int   : Custo associado ao fitness de consumo de combustível
        )
        self.C_cur = C_cur  # int   : Custo associado ao fitness de curvatura da rota
        self.C_t = C_t  # int   : Custo associado ao fitness do tamanho do DNA (T ou horizonte de planejamento)
        self.C_dist = C_dist
        self.max_exec_time = (
            max_exec_time  # float : Tempo máximo de execução - Stop criteria (segundos)
        )
        self.min_precision = (
            min_precision  # float : Precisão mínima de acerto ao destino (metros)
        )
        self.k_tournament = (
            k_tournament  # int   : Quantidade de indivíduos disputando o torneio
        )
        self.gps_imprecision = gps_imprecision  # float : Imprecisão do GPS (metros)
        self.big_delta = big_delta

        # Versionamento
        # version=Version("beta", "RC"),
        # self.version = version

        # Alguns dos valores do kwargs são passados para a instanciação dos indivíduos
        self.kwargs = kwargs

        # Inicialização
        self.population = None
        self.fitnesses = None
        self.best = None
        # self.ancestry = []
        self.history = []
        self.current_id = 0

    def run(self, max_exec_time=None, verbose=False, info=False, debug=False):
        self.max_exec_time = max_exec_time if max_exec_time else self.max_exec_time

        # Acompanhamento do tempo (critério de parada)
        self.start_time = time.time()
        self.generation = 0

        # Genesis
        self.population = self._genesis(self.Specie, self.population_size)

        # Inicializar
        self._decode(self.population)

        # Avaliar
        self.fitnesses = [self._fitness(subject, self.mapa) for subject in self.population]

        # Criar História
        self.history = [subject.to_dict() for subject in self.population]

        # Escolher melhor de todos
        self.best = self.population[self.fitnesses.index(max(self.fitnesses))]

        # self.ancestry.append(self.best)

        # self.trace = []

        while not self.stop_criteria():
            self.flag_newborn = self.population_size

            while not self.converge():
                self.flag_newborn = 0
                self.generation += 1

                for _ in range(ceil(self.taxa_cross * self.population_size)):

                    # Seleção por torneio
                    parent1, parent2 = self._tournament(
                        self.population,
                        k=self.k_tournament
                    )

                    # Crossover
                    child = parent1.crossover(parent2, self.Specie, **self.kwargs)

                    # Mutação
                    child.mutation()

                    # Fitness
                    self._fitness(child, self.mapa)

                    # Adicionar filho na população
                    self._insert(child, parent1, parent2)

            # Reiniciar rotas
            self.population = []
            self.population = self._genesis(self.Specie, self.population_size - 1)

            # Inicializar
            self._decode(self.population)

            # Avaliar
            self.fitnesses = [self._fitness(subject, self.mapa) for subject in self.population]

            # Criar História
            self.history.extend([subject.to_dict() for subject in self.population])

            # Nunca matar o melhor de todos
            self.population.append(self.best)
            self.fitnesses.append(self.best.fitness)

            # Escolher melhor de todos
            self.best = self.population[self.fitnesses.index(max(self.fitnesses))]

            # Print
            #print("Meteoro! Reiniciando rotas")

        return self.best

    # ---

    def _insert(self, child, parent1, parent2):
        # Verifica se um indivíduo é digno de entrar na população e tomar o lugar de um de seus pais

        self.flag_newbest = False

        if child.fitness < parent1.fitness:
            child.set_parents(parent1, parent2)
            self.__substitute(child, parent1)

        elif child.fitness < parent2.fitness:
            child.set_parents(parent2, parent1)
            self.__substitute(child, parent2)

        if child.fitness < self.best.fitness:
            self.best = child
            # self.ancestry.append(child)
            self.flag_newbest = True

    def __substitute(self, child, parent):
        i_parent = self.population.index(parent)

        child.set_generation(self.generation)
        child.set_id(self.current_id)
        self.current_id += 1

        self.population.remove(parent)
        self.population.append(child)

        self.fitnesses.pop(i_parent)
        self.fitnesses.append(child.fitness)
        self.flag_newborn += 1

        self.history.append(child.to_dict())

    # ---

    def stop_criteria(self):
        # Para a execução depois de uma quantidade de segundos
        if (time.time() - self.start_time) >= self.max_exec_time:
            return True
        return False

    def converge(self):
        # Converge caso nenhum novo indivíduo seja adicinado
        if self.flag_newborn == 0:
            return True
        return False

    # ---

    def _genesis(self, Specie, population_size):
        current_id = self.current_id

        population = [
            Specie(
                start_time=self.start_time,
                generation=self.generation,
                id=current_id + i,
                **self.kwargs
            )
            for i in range(population_size)
        ]

        self.current_id = current_id + population_size
        # Removed parameter: version=self.version,
        return population

    # ---

    def _decode(self, population):
        for subject in population:
            subject.decode()
        return True

    # ---

    def _fitness(self, subject, mapa):

        fit_d = self.__fitness_destination(subject, mapa)
        fit_obs = self.__fitness_obstacles(subject, mapa)
        fit_con = self.__fitness_consumption(subject, mapa)
        fit_cur = self.__fitness_curves(subject, mapa)
        fit_t = self.__fitness_t(subject, mapa)
        fit_dist = self.__fitness_distance(subject, mapa)

        fitness_trace = [
            self.C_d * fit_d,
            self.C_obs * fit_obs,
            self.C_con * fit_con,
            self.C_cur * fit_cur,
            self.C_t * fit_t,
            self.C_dist * fit_dist,
        ]

        fitness = sum(fitness_trace)

        subject.set_fitness(fitness, fitness_trace)

        return fitness

    def __fitness_destination(self, subject, mapa):
        # Prioriza rotas que acertem o destino

        A = subject.dna_decoded[-1]  # Último waypoint da rota
        B = mapa.destination  # Waypoint de destino

        # Distância euclidiana entre o último ponto da rota e o ponto de destino
        d = sqrt((B.x - A.x) ** 2 + (B.y - A.y) ** 2)

        # Determina uma precisão mínima aceita
        if d < self.min_precision:  # min_precision default = 1.0
            return 0
        return d

    def __fitness_distance(self, subject, mapa):
        # Prioriza rotas mais curtas

        d = 0
        length = len(subject.dna_decoded)
        for i in range(length - 1):
            A = subject.dna_decoded[i]
            B = subject.dna_decoded[i + 1]
            # Distância euclidiana entre o último ponto da rota e o ponto de destino
            d += sqrt((B.x - A.x) ** 2 + (B.y - A.y) ** 2)

        return d

    def __fitness_obstacles(self, subject, mapa):
        # def __fitness_obstacles_RC(self, subject, mapa):
        # Prioriza rotas que não ultrapassem obstáculos
        count = 0

        for gene_decoded_t1, gene_decoded_t2 in pairwise(subject.dna_decoded):
            # Utiliza somente as áreas infladas para cálculo
            for area_n in mapa.areas_n_inf:
                wp1 = CartesianPoint(gene_decoded_t1.x, gene_decoded_t1.y)
                wp2 = CartesianPoint(gene_decoded_t2.x, gene_decoded_t2.y)

                # Calcula se algum waypoint está dentro de algum obstáculo
                if point_in_polygon(wp1, area_n):
                    count += 1

                # Calcula se alguma conexão entre os waypoints intersecciona algum obstáculo
                if segment_in_polygon(wp1, wp2, area_n):
                    count += 1

        return count
        # def __fitness_obstacles(self, subject, mapa):
        #     # def __fitness_obstacles is an abstraction of either one of those two following functions
        #     # __fitness_obstacles_RC and __fitness_obstacles_CC

        #     if self.version.minor == "RC":
        #         return self.__fitness_obstacles_RC(subject, mapa)

        #     elif self.version.minor == "CC":
        #         return self.__fitness_obstacles_CC(subject, mapa)

        # def __fitness_obstacles_CC(self, subject, mapa):
        #     uncertainty = self.gps_imprecision

        #     # if debug:
        #     #    print('(   x   ,   y   ) distance | risk(%)')

        #     risks_points = []
        #     for gene_decoded in subject.dna_decoded:
        #         risks_areas = []
        #         for area in mapa.areas_n_inf:
        #             wp = CartesianPoint(gene_decoded.x, gene_decoded.y)

        #             distance = _distance_wp_area(wp, area)
        #             risk = _prob_collision(distance, uncertainty)

        #             # if debug:
        #             #    print('({0:^.1f},{1:^.1f}) {2:8.3f} | {3:}'.format(wp.x, wp.y, distance, round(risk,4)))

        #             risks_areas.append(risk)
        #         risks_points.append(sum(risks_areas))

        #     # print(risks_points)
        #     return sum(risks_points)

    def __fitness_consumption(self, subject, _):
        # Prioriza rotas com menor consumo de combustível (bateria)
        consumption = [gene.a ** 2 for gene in subject.dna]
        return sum(consumption)

    def __fitness_curves(self, subject, _):
        # Prioriza rotas que evitem fazer curvas desnecessárias
        curves = [abs(gene.e) for gene in subject.dna]
        return (1 / subject.e_max) * sum(curves)

    def __fitness_t(self, subject, _):
        # Prioriza rotas com menor quantidade de waypoints
        return len(subject.dna)

    # ---

    def _tournament(self, population, k=2):
        parents = []
        for i in range(2):

            local_best = random.choice(population)
            for j in range(k - 1):
                # Seleciona k individuos
                a = random.choice(population)
                if a.fitness < local_best.fitness:
                    local_best = a

            parents.append(local_best)

        # Retorna o resultado de duas batalhas
        return parents[0], parents[1]
