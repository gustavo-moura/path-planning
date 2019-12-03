import collections
import random
import time
import copy

from math import cos, sin, sqrt, ceil

from itertools import tee
from utils import pairwise_circle, point_in_polygon, segment_in_polygon


Gene           = collections.namedtuple('Gene', 'a e')
GeneDecoded    = collections.namedtuple('GeneDecoded', 'x y v al')
CartesianPoint = collections.namedtuple('CartesianPoint', 'x y')



class Subject():
    
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
    
    # Mudanças na função __init__ podem impactar a função generate
    def __init__(
        self,
        px0=10.,
        py0=10.,
        v0=0,
        al0=0,
        v_min=11.1,
        v_max=30.5,
        e_min=-3,
        e_max=3,
        a_min=0.0,
        a_max=2.0,
        T=7,
        delta_T=1.5,
        delta=0.001,
        m=743.0,
        mutation_prob=0.7,
        mutation_rate=0.1,
        spawn_mode='random',
        alpha_BLX=0.1
    ):
        # VANT
        # px0   int : Posição inicial no eixo x (m)
        # py0   int : Posição inicial no eixo y (m)
        # v0    int : Velocidade Inicial (m/s)
        # al0   int : Ângulo inicial (graus)
        self.gene_decoded_0 = GeneDecoded(px0, py0, v0, al0) # GeneDecoded : objeto contendo o gene decodificado 0
        self.v_min = v_min # float : Velocidade máxima (m/s)
        self.v_max = v_max # float : Velocidade mínima (m/s)
        self.e_min = e_min # int   : Velocidade angular mínima (graus/s)
        self.e_max = e_max # int   : Velocidade angular máxima (graus/s)
        self.a_min = a_min # float : Aceleração mínima (m/s**2)
        self.a_max = a_max # float : Aceleração máxima (m/s**2)
        
        # Modelo
        self.T       = T       # int : Horizonte de planejamento (s)
        self.delta_T = delta_T # int : Discretização do tempo (s)
        #self.delta   = delta   # float : Probabilidade de violar Phi_n (-)
        self.m       = m       # float : Massa do VANT (!=0) (gramas)
    
        # Parametros do indivíduo
        self.mutation_prob = mutation_prob # float : Probabilidade de ocorrer uma mutação no dna (%)
        self.mutation_rate = mutation_rate # float : Taxa de mutação no dna (%)
        self.fitness       = None          # float : Fitness do indivíduo
        self.dna           = None          # list  : Conjunto de genes formando o DNA ([Gene, ...])
        self.dna_decoded   = None          # list  : DNA decodificado ([GeneDecoded, ...])
        self.spawn_mode    = spawn_mode    # str   : Tipo de incialização do DNA {'random'}
        self.alpha_BLX     = alpha_BLX     # float : Parametro real constante, usado no crossover BLX alpha
        
        self.spawn(mode=spawn_mode)
    
    
    def set_fitness(self, fitness):
        self.fitness = fitness
        
    # ---
    
    def spawn(self, mode):
        self.dna = [self._build_gene(mode) for i in range(self.T) ]
        
    def _build_gene(self, mode='random'):
        # Inicialização aleatória gera valores com distribuição uniforme
        if mode == 'random':
            a = random.uniform(self.a_min, self.a_max)
            e = random.uniform(self.e_min, self.e_max)
            
        return Gene(a, e)
    
    # ---
    
    def decode(self):
        #self.dna_decoded = [self._decode_gene() for i in range(len(self.dna))]
        self.dna_decoded = self._decode_gene() # TODO: Organizar, voltar como era a linha de cima. Fazer função abaixo só computar o gene
        
    def _decode_gene(self):
        dna = self.dna
        
        # parametros
        delta_T = self.delta_T
        m = self.m
        
        dna_decoded = []
        dna_decoded.append(self.gene_decoded_0)
        
        for i in range(0, len(dna)):
            # dna
            a  = dna[i].a
            e  = dna[i].e
            
            # dna decodificado
            px = dna_decoded[i].x
            py = dna_decoded[i].y
            v  = dna_decoded[i].v
            al = dna_decoded[i].al
            
            F = self.__F(v)
        
            # Equações descritas em (Arantes 2016)
            _px = px + ( v * cos(al) * delta_T ) + ( a * cos(al) * ((delta_T**2)/2) ) 
            _py = py + ( v * sin(al) * delta_T ) + ( a * sin(al) * ((delta_T**2)/2) ) 
            _v  = v  + ( a * delta_T ) - ( (F/m) * delta_T )
            _al = al + ( e * delta_T )

            dna_decoded.append(GeneDecoded(_px, _py, _v, _al))

        return dna_decoded
    
    
    def __F(self, v):
        # Equação do Arrasto
        # Disponível em https://pt.wikipedia.org/wiki/Equa%C3%A7%C3%A3o_do_arrasto
        # Versão utilizada ((Arantes, 2016) equação 3.5)
        
        Cd  = 0.8     # float : Coeficiente de arrasto, específico para cada aeronave
                      #         (considerado Angled Cube) obtido de https://pt.wikipedia.org/wiki/Coeficiente_de_resist%C3%AAncia_aerodin%C3%A2mica
        rho = 1.225   # float : Massa específica do fuído (aka densidade) (k/m**3)
                      #         (a 15 graus Celsius) Valor de rho obtido de https://pt.m.wikipedia.org/wiki/Densidade_do_ar
        A = 1.0       # float : Área de referência # TODO: o que é isso?
        # v = v       # float : Velocidade do Vant no instante t (fornecido como parâmetro da função)
        
        F = 0.5 * Cd * rho * A * (v**2)
        
        return F
        
    
    # ---
    
    def crossover(self, parent2):
        dna = random.choice([self._OX, self._BLX_Alpha])(self.dna, parent2.dna)
        child = self.generate(dna)
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
            
            gene = Gene(a, e)
            dna.append(gene)
            
        return dna
    
    
    def __BLX_ALpha_select_gene(self, x, y):
        # x, y um gene de cada pai
        alpha = self.alpha_BLX
        d = abs(x-y)
        u = random.uniform(min(x,y)-alpha*d, max(x,y)+alpha*d)
        return u
    
    
    def generate(self, dna):
        # Cria um filho com os mesmos parametros do pai, mas com um dna fornecido
        child = copy.deepcopy(self)
        child.dna = dna
        child.decode()
        return child
    
        
    # ---
    
    def mutation(self, mutation_prob=None, mutation_rate=None):
        # Mutação Creep
        mutation_prob = self.mutation_prob if not mutation_prob else mutation_prob
        
        # Tem uma probabilidade mutation_prob de mutar o gene ou não
        if random.random() < mutation_prob:
            
            new_dna = []
            for gene in self.dna:
                a = self._mute(gene.a, self.a_min, self.a_max)
                e = self._mute(gene.e, self.e_min, self.e_max)
                
                # TODO2: otimizar
                new_gene = Gene(a, e)
                new_dna.append(new_gene)
                
                
            self.dna = new_dna
            self.decode()

            
        return True
        
        
    def _mute(self, val, min_val, max_val):
        # TODO2: Entender melhor o 0
        mutation_rate = random.uniform(0, max_val*0.5)
        s = random.choice([1, -1])
        val = val * (1 + (mutation_rate * s))

        # Checar se não estoura os limites
        val = max(val, min_val)
        val = min(val, max_val)

        return val
    
    
    # ---
    
    def get_route(self):
        return [ [gene.x, gene.y] for gene in self.dna_decoded ]



class Genetic():
    
    def __init__(
        self, 
        Specie, 
        mapa,
        taxa_cross=0.5,
        population_size=100,
        C_d=2,
        C_obs=100,
        C_con=10,
        C_cur=3,
        max_exec_time=5,      
    ):
        # Modelo
        self.Specie = Specie # Object class defining the subject provided by user
        self.mapa   = mapa
        
        # Parametros
        self.taxa_cross      = taxa_cross      # int : Taxa de ocorrencia do crossover
        self.population_size = population_size # int : Quantidade máxima de indivíduos na população
        self.C_d   = C_d    # int : Custo associado ao fitness de destino
        self.C_obs = C_obs  # int : Custo associado ao fitness de obstáculos
        self.C_con = C_con  # int : Custo associado ao fitness de consumo de combustível
        self.C_cur = C_cur  # int : Custo associado ao fitness de curvatura da rota
        self.max_exec_time = max_exec_time # float : Tempo máximo de execução - Stop criteria (seconds)
        
        # Inicialização
        self.population = None 
        self.fitnesses  = None
        self.best       = None
        self.ancestry   = []
        
        
        
    def run(self, max_exec_time=None, verbose=False, info=False, debug=False):
        
        self.max_exec_time = max_exec_time if max_exec_time else self.max_exec_time
        
        # Acompanhamento do tempo (criterio de parada)
        self.start_time = time.time()
        
        # Genesis
        self.population = self._genesis(self.Specie, 'random', self.population_size)
        
        # Inicializar
        self._decode(self.population)
        
        # Avaliar
        self.fitnesses = [self._fitness(subject, self.mapa) for subject in self.population]
    
        # Escolher melhor de todos
        self.best = self.population[self.fitnesses.index(max(self.fitnesses))]
        
        self.trace = []
        
        while not self.stop_criteria():
            self.flag_newborn = self.population_size
            
            while not self.converge():
                self.flag_newborn = 0
                
                for _ in range(ceil(self.taxa_cross * self.population_size)):
                    # Seleção
                    parent1, parent2 = self._tournament(self.population)
            
                    
                    # Crossover
                    child = parent1.crossover(parent2)
                    
                    
                    # Mutação
                    child.mutation()
                    
                    
                    # Fitness
                    self._fitness(child, self.mapa)
                    
                    
                    # Adicionar filho na população
                    self._insert(child, parent1, parent2)
                    
                    
                    # Print
                    if verbose and self.flag_newbest:
                        print('  Novo melhor de todos! fit: {}'.format(self.best.fitness))
                    if debug:
                        print('\nparent1.dna', parent1.dna)
                        print('\nparent2.dna', parent2.dna)
                        print('\nchild.dna.mutation', child.dna)
                        
                        
                # TODO2: Eliminar esse recalculo
                self.fitnesses = [self._fitness(subject, self.mapa) for subject in self.population]
                self.trace.append({
                    'medium_fitness': sum(self.fitnesses)/self.population_size,
                    'best_fitness': self.best.fitness,
                    'newborns': self.flag_newborn,
                    'newbest': self.flag_newbest
                })
                
                # Print
                if verbose:
                    print('Fim da geração. {} novos indivíduos'.format(self.flag_newborn))
                    print('Melhor de todos: {}'.format(self.best.fitness))
                    print('-'*20)
                        
            # Reiniciar rotas
            self.population = self._genesis(self.Specie, 'random', self.population_size-1)
            # Nunca matar o melhor de todos
            self.population.append(self.best)
            
            
            # Inicializar
            self._decode(self.population)
            
            
            # Avaliar
            self.fitnesses = [self._fitness(subject, self.mapa) for subject in self.population]
            
            
            
            # Print
            if verbose:
                print('Meteoro! Reiniciando rotas')
            if info:
                print('Meteoro! Melhor de todos:{}'.format(self.best.fitness))
                
        return self.best
                
    # ---
    
    def _insert(self, child, parent1, parent2):
        # Verifica se um indivíduo é digno de entrar na população e tomar o lugar de um de seus pais

        self.flag_newbest = False
        
        if child.fitness < parent1.fitness:
            self.__substitute(child, parent1)

        elif child.fitness < parent2.fitness:
            self.__substitute(child, parent2)

        if child.fitness < self.best.fitness:
            self.best = child
            self.ancestry.append(child)
            self.flag_newbest = True
    
    
    def __substitute(self, child, parent):
        i_parent = self.population.index(parent)

        self.population.remove(parent)
        self.population.append(child)

        self.fitnesses.pop(i_parent)
        self.fitnesses.append(child.fitness)
        self.flag_newborn += 1
    
    
    # ---
    
    def stop_criteria(self):
        # Para a execução depois de uma quantidade de segundos
        if (time.time() - self.start_time) >= self.max_exec_time:
            return True
        else:
            return False
    
    def converge(self):
        # Converge caso nenhum novo indivíduo seja adicinado
        if self.flag_newborn == 0:
            return True
        else:
            return False
                         
    # ---
    
    def _genesis(self, Specie, spawn_mode, population_size):
        population = [Specie(spawn_mode=spawn_mode) for i in range(population_size)]
        return population 
    
    # ---
    
    def _decode(self, population):
        for subject in population:
            subject.decode()
        return True
    
    # ---
    
    def _fitness(self, subject, mapa):
        
        fit_d   = self.__fitness_destination(subject, mapa)
        fit_obs = self.__fitness_obstacles(subject, mapa)
        fit_con = self.__fitness_consumption(subject, mapa)
        fit_cur = self.__fitness_curves(subject, mapa)
        
        fitness = (self.C_d   * fit_d 
                 + self.C_obs * fit_obs
                 + self.C_con * fit_con
                 + self.C_cur * fit_cur)
        
        #fitness = round(fitness, 8)
        
        subject.set_fitness(fitness)
        
        return fitness
    
    def __fitness_destination(self, subject, mapa):
        # Prioriza rotas que acertem o destino
        # Distância euclidiana entre o último ponto da rota e o ponto de destino
        A = subject.dna_decoded[-1]
        B = mapa.destination
        
        return sqrt( (B.x - A.x)**2 + (B.y - A.y)**2 )
    
    def __fitness_obstacles(self, subject, mapa):
        # Prioriza rotas que não ultrapassem obstáculos
        # Não bater em obstáculos
        count = 0
        
        for gene_decoded_t1, gene_decoded_t2  in pairwise_circle(subject.dna_decoded):
            for area_n in mapa.areas_n:
                wp1 = CartesianPoint(gene_decoded_t1.x, gene_decoded_t1.y)
                if point_in_polygon(wp1, area_n):
                    count += 1
                    
                wp2 = CartesianPoint(gene_decoded_t2.x, gene_decoded_t2.y)
                if segment_in_polygon(wp1, wp2, area_n):
                    count += 1
            
        return count
    
    
    def __fitness_consumption(self, subject, _):
        # Prioriza rotas com menor consumo de combustível (bateria)
        consumption = [gene.a**2 for gene in subject.dna]
        return sum(consumption)
    
        
    def __fitness_curves(self, subject, _):
        # Prioriza rotas que evitem fazer curvas desnecessárias
        curves = [abs(gene.e) for gene in subject.dna]
        return (1/subject.e_max) * sum(curves)
        
    # ---
        
    def _tournament(self, population, k=2):
        parents = []
        for _ in range(2):
            
            local_best = random.choice(population)
            for _ in range(k-1):
                # Seleciona k individuos
                a = random.choice(population)
                if a.fitness > local_best.fitness:
                    local_best = a
                    
            parents.append(local_best)
            
        # Retorna o resultado de duas batalhas
        return parents[0], parents[1]
        
        

class Mapa():
    # TODO: Melhorar
    def __init__(self, origin, destination, areas_n):
        self.origin = origin # CartesianPoint(origin[0], origin[1]) # (x, y)
        self.destination = destination # CartesianPoint(destination[0], destination[1]) # (x, y)
        self.areas_n = areas_n # [area, ...]
        


class Area():
    def __init__(self, vertices):
        self.vertices = vertices

