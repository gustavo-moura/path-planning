from collections import namedtuple

from scipy.special import erf
import numpy as np
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



# ------- Function to decodify the subject

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




# ------- Objective function

def objective_function(subject, mapa):
    # Minimizar a função objetivo

    x = subject.x

    K = len(x)-1 # posição final

    vk = x[K].v


    print(x[K], mapa)


    fit = [f_pouso_b(x[K], mapa),
        f_pouso_p(x[K], mapa), 
        f_pouso_voo_n(x, mapa), 
        f_curvas(subject),
        f_dist(),      # Desativado
        f_viol(vk), 
        f_bat(K)        # Desativado
    ]

    fitness = sum(fit)

    print(fit)
    print(fitness)
    exit()

    return fitness




# ------- Intermediary functions

def f_pouso_b(x, mapa): # 4.3
    # Define recompensa em caso de pouso em regiões bonificadoras.
    # custo * somatoria da probabilidade de pousar em cada uma das regiões bonificadoras
    res = -Cb * Somatoria(Pr_x_E_Z, x, mapa.bonificadoras)
    print(Somatoria(Pr_x_E_Z, x, mapa.bonificadoras))
    return res
    

def f_pouso_p(x, mapa): # 4.4
    # Define punição em caso de pouso em regiões penalizadoras.
   
    return Cp * Somatoria(Pr_x_E_Z, x, mapa.penalizadoras)


def f_pouso_voo_n(x, mapa): # 4.5
    # Penaliza o pouso ou voo da aeronave sobre regiões não navegáveis.    
   
    calc = 1 - delta - Somatoria_dupla(Pr_x_E_Z, x, mapa.nao_navegaveis)
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
        f = func(x, Z)
        print("f: ", f)
        soma += f

    return min(soma, 1)


def Somatoria_dupla(func, xs, Zs):
    soma = 0

    for x in xs:
        for Z in Zs:
            soma += func(x, Z)

    return min(soma, 1)




# ------- Chance of collision, probability


def chance_of_collision(X, Z):
    # seja X um ponto e Z uma área

    # Z.points = [p1, p2, p3, p4]
    # p.x p.y p.z

    maior = -99999999 

    edges = Z.get_edges()
    for edge in edges:
        normal_vector = normal(edge.A, edge.B)

        delta_y = normal_vector[0]
        delta_x = normal_vector[1]

        b = delta_y * edge.A.x + delta_x * edge.A.y  # Curva de nível (?)
        P0=100
        R = math.sqrt(2 * np.sum(np.power(normal_vector, 2)) * P0)
        chance = (delta_y * X.x + delta_x * X.y - b) / R
        print('chance: ', chance)
        maior = max(chance, maior)
        print(maior)
    print('erf', erf(maior))
    delta = (1 - erf(maior)) / 2
    print("delta: ", delta)
    #return l == inst.L -1 ? 2*delta : del
    return delta


def normal(A, B):
    # plano determinado pela equação ax + by + cz + d = 0, onde (a, b, c) é o vetor normal

    x = (A.x - B.x)
    y = (A.y - B.y)

    # direction_vector = (x, y) # vector in the same direction of the line that connects A and B
    normal_vector = (-y, x) # rotate the direction vector by 90º. (x, y) -> (-y, x) 

    normal = np.array([normal_vector[0], normal_vector[1], 0, 0, 0, 0])

    return normal


def Pr_x_E_Z(X, Z):
    chance = chance_of_collision(X, Z)
    return min(chance, 1)


