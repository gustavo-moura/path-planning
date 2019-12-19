import itertools
import math
from scipy.stats import norm

from genetic.data_definitions import Vector

# Support Functions
# _________________________________________________________________________________________________


def pairwise_circle(iterable):
    """Iterates over an iterable object, matching pairwise elements and repeating the first.
    s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)
    """
    a, b = itertools.tee(iterable)
    first_value = next(b, None)
    return itertools.zip_longest(a, b, fillvalue=first_value)


def pairwise(iterable):
    """Iterates over an iterable object, matching pairwise elements.
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def boundary(val, val_min, val_max):
    """Clips a value to stay within the range [val_min; val_max]."""
    return max(min(val, val_max), val_min)


# Ray Casting Algorithm
# _________________________________________________________________________________________________
epsilon = 0.00001  # Used on the Ray-Tracing Algorithm


def point_in_polygon(point, polygon):
    """Checks if a given point is within the polygon provided.

    Args:
        point (CartesianPoint): A point to check if it is within a polygon.
        polygon (List[CartesianPoints]): The polygon formed by a list containing many vertexs. Each vertex is a CartesianPoint.

    Returns:
         bool: True if it is inside the polygon, False otherwise.
    """

    # Arguments:
    #     point {CartesianPoint} --
    #     polygon {List[CartesianPoints]} -- The polygon formed by a list containing many vertexs. Each vertex is a CartesianPoint.

    #
    # """
    # """Using Ray Casting algorithm (inspired by: https://rosettacode.org/wiki/Ray-casting_algorithm, last accessed on 18.12.19)."""

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
    """Executes the Ray Casting algorithm to check if the a given ray intersects the segment.

    Arguments:
        P {CartesianPoint} -- The point from which the ray starts. The ray shall start on this point and move horizontally increasing along the X axis (i.e. to the right).
        A {CartesianPoint} -- The end-point of the segment with the smallest y coordinate.
                              (A must be "below" B)
        B {CartesianPoint} -- The end-point of the segment with the greatest y coordinate.
                              (B must be "above" A)

    Returns:
        Boolean -- True if the ray is intersecting the segment, False otherwise.
    """

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
    """Iterates over each polygon's edge to check if it intersects with the provided segment formed by wp1 and wp2.

    Arguments:
        wp1 {CartesianPoint} -- The end-point of the segment.
        wp2 {CartesianPoint} -- The end-point of the segment.
        polygon {List[CartesianPoints]} -- The polygon formed by a list containing many vertexs. Each vertex is a CartesianPoint.

    Returns:
        Boolean -- True if it is intersecting at least one edge of the polygon, False otherwise.
    """

    for vertex1, vertex2 in pairwise_circle(polygon):
        if segment_intersects_segment(wp1, wp2, vertex1, vertex2):
            return True
    return False


def segment_intersects_segment(p1, q1, p2, q2):
    """Checks the intesection between two segments by performing a series of checks.
        Segment 1: (p1,q1)
        Segment 2: (p2,q2)

    Arguments:
        p1 {CartesianPoint} -- The end-point of the segment 1.
        q1 {CartesianPoint} -- The end-point of the segment 1.
        p2 {CartesianPoint} -- The end-point of the segment 2.
        q2 {CartesianPoint} -- The end-point of the segment 2.

    Returns:
        [type] -- [description]
    """
    """ Two segments (p1,q1) and (p2,q2) intersect if and only if one of the following two conditions is verified:

        1. General Case:
        – (p1, q1, p2) and (p1, q1, q2) have different orientations and
        – (p2, q2, p1) and (p2, q2, q1) have different orientations.

        2. Special Case
        – (p1, q1, p2), (p1, q1, q2), (p2, q2, p1), and (p2, q2, q1) are all collinear and
        – the x-projections of (p1, q1) and (p2, q2) intersect
        – the y-projections of (p1, q1) and (p2, q2) intersect
    """
    """Inspired by: https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/, last accessed on 18.12.19"""

    # Find the four orientations needed for general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

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
    """Given three colinear points p, q, r, the function checks if point q lies on line segment 'pr'."""
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
    """Find orientation of ordered triplet (p, q, r).

    Returns:
        0 --> p, q and r are colinear
        1 --> Clockwise
        2 --> Counterclockwise
    """
    """See https://www.geeksforgeeks.org/orientation-3-ordered-points/ (last accessed on 18.12.19) for details of below formula."""

    val = (q.y - p.y) * (r.x - q.x) - ((q.x - p.x) * (r.y - q.y))

    if val == 0:
        return 0  # colinear

    return 1 if val > 0 else 2  # clock or counterclock wise


# Chance Constraint
# _________________________________________________________________________________________________


def _distance_wp_area(wp, area):
    """Calculates the distance between one point wp and an area area."""
    max_distance = -math.inf

    for A, B in pairwise_circle(area):
        distance = _distance_wp_line(wp, A, B)
        max_distance = max(max_distance, distance)

    return max_distance


def _distance_wp_line(P, A, B, return_norm=False):
    """Calculates the distance between the point P and the line that crosses A and B."""

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
    if return_norm:
        return dist, N
    return dist


def _prob_collision(distance, uncertainty):
    """Survival function (also defined as 1 - cdf, but sf is sometimes more accurate)."""
    """Details available on https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html, last accessed on 18.12.19."""

    # mi    : média         : location
    # sigma : desvio padrão : scale

    return norm.sf(distance, loc=0, scale=uncertainty)
