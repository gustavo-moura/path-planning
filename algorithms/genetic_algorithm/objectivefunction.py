from collections import namedtuple

import math

# Used on the Ray-Tracing Algorithm
epsilon = 0.00001 


# Com base na página 106 da tese de mestrado do Jesimar
# Modelo
# T = 60
deltaT = 1
delta = 0.001
e_min = -3
e_max = 3

# Pesos
Cb = 2000
Cp = 8000
Cn = 100000
Cr = 0

vmin = 11.1



# MINIMIZAR
def transitar_(subject, t):
    # Realiza a decodificação da transição entre os tempos t e t+1
    # Representa as mudanças de estados do VANT


    # Parâmetros:
    # Assumindo valor fixo
    Fd = 1 # Resistência do ar ou força do arrasto # Equação 3.5
    
    # Assumindo valor fixo
    deltaT = 1 # Discretização do tempo com intervalo de tempo fixo

    # Assumindo valor fixo
    m = 1 # ? # ToDo: OQUEÉISSO?


    # Variáveis de Decisão:
    x = subject.x[t]        # Conjunto de estados do VANT
    px = x[0]               #   Posição no eixo x
    py = x[1]               #   Posição no eixo y
    v = x[2]                #   Velocidade horizontal
    al = x[3]               #   Ângulo horizontal

    u = subject.dna[t]      # Conjunto de controles
    a = u[0]                #   Aceleração
    e = u[1]                #   Variação angular


    # Função de Transição:
    px_ = px + v * math.cos(al) * deltaT + a * math.cos(al) * (deltaT**2)/2
    py_ = py + v * math.sin(al) * deltaT + a * math.sin(al) * (deltaT**2)/2
    v_ = v + a * deltaT - (Fd/m) * deltaT
    al_ = a + e * deltaT 


    control = namedtuple('control', 'x y v a')

    return control(px_, py_, v_, al_)




def objective_function(subject, mapa):
    # Minimizar a função objetivo

    x = subject.x

    K = len(x)-1 # posição final

    vk = x[K].v

    fit = [f_pouso_b(x[K], mapa),
        f_pouso_p(x[K], mapa), 
        f_pouso_voo_n(x, mapa), 
        f_curvas(subject),
        f_dist(),      # Desativado
        f_viol(vk), 
        f_bat(K)        # Desativado
    ]

    fitness = sum(fit)

    # print(fit)
    # print(fitness)
    # #exit()

    return fitness


# ------- Intermediary functions

def f_pouso_b(x, mapa): # 4.3
    # Define recompensa em caso de pouso em regiões bonificadoras.
    # custo * somatoria da probabilidade de pousar em cada uma das regiões bonificadoras
   
    return -Cb * Somatoria(Pr_x_E_Z, x, mapa.bonificadoras)
    

def f_pouso_p(x, mapa): # 4.4
    # Define punição em caso de pouso em regiões penalizadoras.
   
    return Cp * Somatoria(Pr_x_E_Z, x, mapa.penalizadoras)


def f_pouso_voo_n(x, mapa): # 4.5
    # Penaliza o pouso ou voo da aeronave sobre regiões não navegáveis.    
   
    calc = 1 - delta - Somatoria_dupla(Pr_x_nE_Z, x, mapa.nao_navegaveis)
    return Cn * max(0, calc)

    
def f_curvas(subject): # 4.6
    # Prioriza rotas que evitem fazer curvas desnecessárias.
    es = [gene[1] for gene in subject.dna]

    return (1/e_max) * sum(es)


def f_dist(): # 4.7
    # Dá mais chance a rotas com menores distâncias das regiões bonificadoras.
    return 0


def f_viol(vk): # 4.8
    # Se a aeronave tem velocidade final maior do que o seu valor mínimo, não ocorre de fato
    # um pouso. Dessa maneira, a Equação (f_viol) evita rotas em que o VANT não consegue pousar,
    # mesmo que atinja uma região bonificadora.
    if vk - vmin > 0:
        return Cb
    else:
        return 0


def f_bat(K): # 4.9
    # Se houver um problema na bateria, a Equação (f_bat) é adicionada à função de fitness. O
    # objetivo é reduzir o tempo de voo, assim a aeronave buscará regiões para pouso mais próximas
    # de sua localização no momento onde ocorreu a pane.
    #return Cb * (2 ** ((K-T)/10) )
    return 0

# ------- Auxiliary functions

def Somatoria(func, x, Zs):
    soma = 0

    for Z in Zs:
        soma += func(x, Z.points)

    return soma


def Somatoria_dupla(func, xs, Zs):
    soma = 0

    for x in xs:
        for Z in Zs:
            soma += func(x, Z.points)

    return soma


# Deprecated
def deprecated_Pr_x_E_Z(x, Z):
    # print()
    # print(x)
    # for p in Z:
    #     print(p.x, p.y, p.z)

    if point_in_polygon(x, Z):    
        # print("SIM")
        # print()
        # print(x)
        # for p in Z:
        #     print(p.x, p.y, p.z)
        return 1
    else:
        # print("NAO")
        return 0

def Pr_x_E_Z(x, Z):


def chance_of_collision(X, Z):
    # seja x um ponto e Z uma área

    # Z.points = [p1, p2, p3, p4]
    # p.x p.y p.z

    edges = Z.get_edges()
    for edge in edges:
        delta_y = - (edge.A.y - edge.B.y)
        delta_x = + (edge.A.x - edge.B.x)

        b = delta_y * edge.A.x + delta_x * edge.A.y  # Curva de nível (?)


        R = sqrt(2 * sum(a**2) * P0)

        chance = (delta_y * x + delta_x * y - b) / R

        



def normal(A, B):
    # plano determinado pela equação ax + by + cz + d = 0, onde (a, b, c) é o vetor normal

    x = (A.x - B.x)
    y = (A.y - B.y)

    # direction_vector = (x, y) # vector in the same direction of the line that connects A and B
    normal_vector = (-y, x) # rotate the direction vector by 90º. (x, y) -> (-y, x) 

    normal = (normal_vector[0], normal_vector[1], c, 0, 0, 0)

    return normal


def Pr_x_nE_Z(x, Z):
    if not point_in_polygon(x, Z):
        return 1
    else:
        return 0


# -------


def point_in_polygon(point, polygon):
    # Using ray_casting algorithm
    # https://rosettacode.org/wiki/Ray-casting_algorithm
    count = 0

    for i in range(len(polygon) - 1):
        vertex1 = polygon[i]
        vertex2 = polygon[i-1]

        if vertex1.y < vertex2.y:
            A = vertex1
            B = vertex2
        else:
            A = vertex2
            B = vertex1

        if ray_intersects_segment(point, A, B):
            count += 1
    # print("count", count)
    if count!=0 and count % 2 == 0: # Odd
        return True # Inside the polygon
    else:
        return False


def ray_intersects_segment(P, A, B):
    # P : the point from which the ray starts
    # A : the end-point of the segment with the smallest y coordinate
    #     (A must be "below" B)
    # B : the end-point of the segment with the greatest y coordinate
    #     (B must be "above" A)

    # To avoid the "ray on vertex" problem, the point is moved upward of a small quantity epsilon.
    if P.y == A.y or P.y == B.y:
        P.y += epsilon

    # Point higher or lower than polygon
    if P.y < A.y or P[1] > B.y:
        return False

    # Point to the right of the polygon
    elif P.x >= max(A.x, B.x):
        return False 

    else:

        if P.x < min(A.x, B.x):
            return True

        else:

            if A.x != B.x:
                m_red = (B.y - A.y)/(B.x - A.x)
            else:
                m_red = 99999999 # Infinite


            if A.x != P.x:
                m_blue = (P.y - A.y)/(P.x - A.x)
            else:
                m_blue = 99999999 # Infinite


            if m_blue >= m_red:
                return True
            else:
                return False


# ------- Implementação do Calculo de chance de colisão


def prob_of_fail(x, y, areas):
    prob_of_fail = 0

    x = # Posição atual do Drone no eixo x
    y = # Posição atual do Drone no eixo y

    for area in areas:
        chance = chance_of_collision()
        prob_of_fail += min(chance, 1)

    prob_of_fail = min(prob_of_fail, 1)

    return prob_of_fail



def chance_of_collision():

    maior = 

    for lado in polygon:
        
        delta_y = 
        

        exp = (x * delta_y + y * delta_x - b) / R
        maior = max(exp, maior)



    Risco = Normal.standardTailProb(maior, false)
    delta = (1 - Risco) / 2

    return l == inst.L -1 ? 2*delta : delta


    return chance





# --------


for poligono in mapa: # poligono j
    for aresta in poligono: # aresta i

        normal = (a1, a2, a3, 0, 0, 0)






