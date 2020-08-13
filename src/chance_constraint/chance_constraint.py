import itertools
from scipy.stats import norm
from collections import namedtuple
import math
import numpy as np

from src.chance_constraint.model import CartesianPoint, Vector
from src.chance_constraint.visualization import plot_map


# CartesianPoint = namedtuple('CartesianPoint', 'x y')
# Vector = namedtuple('Vector', 'x y')


def pairwise_circle(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)"
    a, b = itertools.tee(iterable)
    first_value = next(b, None)
    return itertools.zip_longest(a, b,fillvalue=first_value)

def prob_collision(distance, uncertainty):
    # Survival function (also defined as 1 - cdf, but sf is sometimes more accurate).
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html

    # mi    : média         : location (loc)
    # sigma : desvio padrão : scale

    return norm.sf(distance, loc=0, scale=uncertainty)

def distance_point_line(P, A, B, return_normal=False):
    '''Calculates the distance between the point P and the line that crosses the points A and B'''

    # Director vector of line
    D = Vector((A.x - B.x), (A.y - B.y))

    # Normal vector of line
    #N = Vector(-D.y, D.x)

    # Normalized normal vector of line AB
    aux = (math.sqrt(D.y**2+D.x**2))
    N = Vector( (D.y/aux), ((-D.x)/aux) )


    b = N.x * A.x + N.y * A.y

    distance = P.x * N.x + P.y * N.y - b

    if return_normal:
        return distance, N

    return distance

def chance_constraint(P, obs):
    distances = []

    for A, B in pairwise_circle(obs):
        aux_distance = distance_point_line(P, A, B)
        distances.append(aux_distance)


    distance = max(distances)
    uncertainty = 1 # GPS imprecision

    chance = prob_collision(distance, uncertainty)
    return chance