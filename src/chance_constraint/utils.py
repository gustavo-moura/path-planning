import itertools
import collections
from scipy.stats import norm

import math

Vector = collections.namedtuple("Vector", "x y")

# Support Functions
# _________________________________________________________________________________________________
def pairwise_circle(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)"
    a, b = itertools.tee(iterable)
    first_value = next(b, None)
    return itertools.zip_longest(a, b, fillvalue=first_value)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def boundary(val, val_min, val_max):
    if val < val_min:
        return val_min
    if val > val_max:
        return val_max
    return val


# Ray Casting Algorithm
# _________________________________________________________________________________________________
epsilon = 0.00001  # Used on the Ray-Tracing Algorithm


def point_in_polygon(point, polygon):
    # Using ray_casting algorithm
    # https://rosettacode.org/wiki/Ray-casting_algorithm

    count = 0

    for vertex1, vertex2 in pairwise_circle(polygon):

        if vertex1.y < vertex2.y:
            A = vertex1
            B = vertex2
        else:
            A = vertex2
            B = vertex1

        if ray_intersects_segment(point, A, B):
            count += 1

    if count % 2 == 0:  # Odd
        return False
    else:
        return True  # Inside the polygon


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
    if P.y < A.y or P.y > B.y:
        return False

    # Point to the right of the polygon
    elif P.x >= max(A.x, B.x):
        return False

    else:

        if P.x < min(A.x, B.x):
            return True

        else:

            if A.x != B.x:
                m_red = (B.y - A.y) / (B.x - A.x)
            else:
                m_red = 99999999  # Infinite

            if A.x != P.x:
                m_blue = (P.y - A.y) / (P.x - A.x)
            else:
                m_blue = 99999999  # Infinite

            if m_blue >= m_red:
                return True
            else:
                return False


# Segment Intersection
# _________________________________________________________________________________________________
def segment_in_polygon(wp1, wp2, polygon):
    # count = 0
    # print('Segment: {}-{}'.format(wp1,wp2))

    for vertex1, vertex2 in pairwise_circle(polygon):
        A = vertex1
        B = vertex2
        # if vertex1.y < vertex2.y:
        #    A = vertex1
        #    B = vertex2
        # else:
        #    A = vertex2
        #    B = vertex1
        # print('Polygon edge: {}-{}'.format(A, B))

        if segment_intersects_segment(wp1, wp2, A, B):
            return True
    return False
    # if count > 1:
    #     return True
    # else:
    #     return False


def segment_intersects_segment(p1, q1, p2, q2):
    # Returns true if line segment 'p1q1' and 'p2q2' intersect.
    # Based on the algorithm from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

    # Two segments (p1,q1) and (p2,q2) intersect if and only if one of the following two conditions is verified:
    #
    # 1. General Case:
    # – (p1, q1, p2) and (p1, q1, q2) have different orientations and
    # – (p2, q2, p1) and (p2, q2, q1) have different orientations.
    #
    # 2. Special Case
    # – (p1, q1, p2), (p1, q1, q2), (p2, q2, p1), and (p2, q2, q1) are all collinear and
    # – the x-projections of (p1, q1) and (p2, q2) intersect
    # – the y-projections of (p1, q1) and (p2, q2) intersect

    # Find the four orientations needed for general and
    # special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    # print(p2, q2, p1, o3)
    o4 = orientation(p2, q2, q1)
    # print(o1,o2,o3,o4)

    # 1. General case
    if o1 != o2 and o3 != o4:
        return True

    # 2. Special Cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    # p1, q1 and q2 are colinear and q2 lies on segment p1q1
    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    # Doesn't fall in any of the above cases
    return False


def on_segment(p, q, r):
    # Given three colinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    if (
        q.x <= max(p.x, r.x)
        and q.x >= min(p.x, r.x)
        and q.y <= max(p.y, r.y)
        and q.y >= min(p.y, r.y)
    ):
        return True
    else:
        return False


def orientation(p, q, r):
    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are colinear
    # 1 --> Clockwise
    # 2 --> Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/
    # for details of below formula.

    val = (q.y - p.y) * (r.x - q.x) - ((q.x - p.x) * (r.y - q.y))
    # print('\n---\ndebug')
    # print((q.y - p.y), (r.x - q.x), (q.x - p.x), (r.y - q.y))
    # print(val)
    if val == 0:
        return 0  # colinear

    return 1 if val > 0 else 2  # clock or counterclock wise


# Chance Constraint
# _________________________________________________________________________________________________
def _distance_wp_area(wp, area):
    # Calculates the distance between one point P and an area area
    max_distance = -math.inf

    for A, B in pairwise_circle(area):
        distance = _distance_wp_line(wp, A, B)
        max_distance = max(max_distance, distance)

    return max_distance


def _normal(A, B):
    # Director vector
    D = Vector((A.x - B.x), (A.y - B.y))

    # Normalized normal vector of line AB
    aux = (math.sqrt(D.y ** 2 + D.x ** 2)) + 1 * 10 ** (-8)
    N = Vector((D.y) / aux, (-D.x) / aux)

    return N


def _distance_wp_line(P, A, B):
    # Calculates the distance between the point P and the line that crosses A and B

    #     # Director vector
    #     D = Vector((A.x-B.x),(A.y-B.y))

    #     # Normal vector of line AB
    #     # N = Vector(-D.y, D.x)

    #     # Normalized normal vector of line AB
    #     aux = (math.sqrt(D.y**2+D.x**2))+1*10**(-8)
    #     N = Vector( (D.y)/aux, (-D.x)/aux )
    N = _normal(A, B)

    b = N.x * A.x + N.y * A.y

    dist = P.x * N.x + P.y * N.y - b

    # if debug:
    #   print(A, B, P, dist)

    return dist


def d_distance_wp_line(P, A, B):
    # Calculates the distance between the point P and the line that crosses A and B

    # Director vector
    D = Vector((A.x - B.x), (A.y - B.y))

    # Normal vector of line AB
    # N = Vector(-D.y, D.x)

    # Normalized normal vector of line AB
    aux = (math.sqrt(D.y ** 2 + D.x ** 2)) + 1 * 10 ** (-8)
    N = Vector((D.y) / aux, (-D.x) / aux)

    b = N.x * A.x + N.y * A.y

    dist = P.x * N.x + P.y * N.y - b

    # if debug:
    #   print(A, B, P, dist)

    return dist, N


def _prob_collision(distance, uncertainty):
    # Survival function (also defined as 1 - cdf, but sf is sometimes more accurate).
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html

    # mi    : média         : location
    # sigma : desvio padrão : scale

    return norm.sf(distance, loc=0, scale=uncertainty)


# Area Inflation
# _________________________________________________________________________________________________

# using general equation of line
def _eq_line(P, Q):
    # general equation of line that intersect two points P and Q
    # https://stackoverflow.com/questions/13242738/how-can-i-find-the-general-form-equation-of-a-line-from-two-points

    # Ax + By + C = 0

    A = P.y - Q.y
    B = Q.x - P.x
    C = (P.x * Q.y) - (Q.x * P.y)

    return A, B, C


def _eq_intersection_point(a, b, c, j, k, l):
    # find the intersection point of two lines, given their general equation arguments
    # https://stackoverflow.com/questions/13244666/how-can-i-find-the-intersection-of-two-lines-in-general-equation-form

    aux = b * j - a * k

    y = (a * l - c * j) / aux
    x = (c * k - b * l) / aux

    return x, y


def euclidean_distance(A, B):
    return math.sqrt((B.x - A.x) ** 2 + (B.y - A.y) ** 2)
