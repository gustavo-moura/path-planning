import math
import json


# ---
# Main functions


def json_to_pddl(map_json_filename, map_id, mission_json_filename, mission_id, output_filename, verbose=False):
    """Converts a json data structure of Map and Mission to PDDL constraints

    Args:
        map_json_filename (str): the filename for the reference map json file, following the structure determined by Drone_arch.
        map_id (int): the index in the list of previous file for the map to be considered.
        mission_json_filename (str): the filename for the reference mission json file, following the structure determined by Drone_arch.
        mission_id (int): the index in the list of previous file for the mission to be considered.
        output_filename (str): the filename in which the conversion's output will be saved. String must end with ".txt" extensions to be saved correctly.
        verbose (bool, optional): activate the verbose mode. Defaults to False.
    """
    print('\n\nStarting conversion...')

    if verbose:
        print(
            f'\n'
            f'Args received:\n'
            f'    map_json_filename: <{map_json_filename}>\n'
            f'    map_id: <{map_id}>\n'
            f'    mission_json_filename: <{mission_json_filename}>\n'
            f'    mission_id: <{mission_id}>\n'
            f'    output_filename: <{output_filename}>\n'
            f'    verbose: <{verbose}>\n'
        )

    with open(map_json_filename, 'r') as f:
        mapa_json = json.load(f)[map_id]

    with open(mission_json_filename, 'r') as f:
        missao_json = json.load(f)[mission_id]

    regions, names, labels, geo_home = read_json(missao_json, mapa_json)

    write_output(output_filename, mapa_json, missao_json, regions, names, labels, geo_home)

    print('\n\nConversion completed.')


def write_output(output_filename, mapa_json, missao_json, regions, names, labels, geo_home):
    """ Coverts and write PDDL output to a file

    Args:
        output_filename ([type]): [description]
    """

    with open(output_filename, "w") as file:

        inputs = ["input1", "input2", "input3", "input4"]

        distances = list_to_str(format_distances(calc_distances(regions), names), sufix="\n        ")
        caminhos = list_to_str(format_caminhos(names))

        string = f"""\
(define (problem rover-2)
    (:domain
        rover-domain
    )

    (:objects

        {list_to_str(get_regions(missao_json))}

        {list_to_str(get_bases(mapa_json))}

        {list_to_str(inputs)}

        {list_to_str(get_objectives(missao_json, command='pulverize', sufix='_objective'))}

        {list_to_str(get_objectives(missao_json, command='take_picture', sufix='_photo'))}

        camera1

        rover1
    )

    (:init
        (rover rover1)
        ;(payload rover1 camera)
        (at rover1 {get_bases(mapa_json)[0]})

        (payload camera1)

        (= (battery-capacity rover1) 100)
        (= (velocity rover1) 7)
        (= (battery-amount rover1) 0)
        (= (recharge-rate-battery rover1) 20)
        (= (discharge-rate-battery rover1) 0.01)
        (= (input-amount rover1) 0)
        (= (input-per-flight rover1) 1)
        ;(can-recharge drone1)

        ;; quanto de cada insumo o drone pode levar
        (= (input-capacity rover1 input1) 10)
        (= (input-capacity rover1 input2) 8)
        (= (input-capacity rover1 input3) 6)
        (= (input-capacity rover1 input4) 4)

        ;; distancias
        {distances}

        ;; regioes q podem ir de uma para outra
        {caminhos}

        ;; definindo as bases
        {list_to_str([f'(base {b})' for b in get_bases(mapa_json)])}

        ;; objetivos de foto
        {list_to_str(get_specific_objective(regions, labels, 'take_picture', 'photo', sufix='_photo'))}

        ;; relação de objetivos de foto com regioes
        {list_to_str([f'(is-visible {i} {j})' for i in get_objectives(missao_json, command='take_picture', sufix='_photo') for j in get_objectives(missao_json, command='take_picture', sufix='')])}

        ;; tipos de insumos
        (input input1) (input input2) (input input3) (input input4)

        ;; objetivos de pulverização
        {list_to_str(get_specific_objective(regions, labels, 'pulverize', 'objective', sufix='_objective'))}

        ;; relação entre regioes e objetivos de pulverização
        {list_to_str([f'(is-in {i} {j})' for i in get_objectives(missao_json, command='pulverize', sufix='_objective') for j in get_objectives(missao_json, command='pulverize', sufix='')])}


        {list_to_str([f'(is-in {i} {b})' for i in inputs for b in get_bases(mapa_json)])}

        {list_to_str([f'(is-recharging-dock {b})' for b in get_bases(mapa_json)])}
        {list_to_str([f'(is-dropping-dock {b})' for b in get_bases(mapa_json)])}
    )

    (:goal
        (and

        {list_to_str([f'(pulverized {i} {b})' for i in inputs for b in get_objectives(missao_json, command='pulverize', sufix='_objective')], prefix=' ;', last_prefix=' ;', diff=True)}
        {list_to_str([f'(taken-image {b})' for b in get_objectives(missao_json, command='take_picture', sufix='_photo')], prefix=' ;', last_prefix=' ;', diff=True)}

        {f'(at rover1 {get_bases(mapa_json)[0]})'}
        )
    )

    (:metric
        minimize (total-time)
    )
)
"""

        file.write(string)


# ---
# Classes


class Region:
    def __init__(self, idi, name, geo_points, cart_points, geo_center, cart_center):
        self.idi = idi
        self.name = name
        self.geo_points = geo_points
        self.points = cart_points
        self.geo_center = geo_center
        self.cart_center = cart_center


class CartesianPoint:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"


class GeoPoint:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


# ---
# Utils


def geo_to_cart(geo_point, geo_home):
    def calc_y(lat, lat_):
        return (lat - lat_) * (10000000.0 / 90)

    def calc_x(longi, longi_, lat_):
        return (longi - longi_) * (
            6400000.0 * (math.cos(lat_ * math.pi / 180) * 2 * math.pi / 360)
        )

    x = calc_x(geo_point.longitude, geo_home.longitude, geo_home.latitude)
    y = calc_y(geo_point.latitude, geo_home.latitude)

    return CartesianPoint(x, y, geo_point.altitude)
    # return CartesianPoint(x, y)


def cart_to_geo(cartesian_point, geo_home):
    def calc_latitude_y(lat_, y):
        return ((y * 90) / 10000000.0) + lat_

    def calc_longitude_x(lat_, longi_, x):
        return ((x * 90) / (10008000 * math.cos(lat_ * math.pi / 180))) + longi_

    longitude_x = calc_longitude_x(
        geo_home.latitude, geo_home.longitude, cartesian_point.x
    )
    latitude_y = calc_latitude_y(geo_home.latitude, cartesian_point.y)

    return GeoPoint(longitude_x, latitude_y, cartesian_point.z)
    # return GeoPoint(longitude_x, latitude_y, 10)


def get_specific_objective(regions, labels, key, word, sufix=""):
    out = []

    for region, label in zip(regions, labels):
        if label == key:
            out.append(f"({word} {region.name+sufix})")

    return out


def calc_distances(regions):
    distances = []
    for ri in regions:
        distance = []
        for rj in regions:
            distance.append(euclidean_distance(ri.cart_center, rj.cart_center))
        distances.append(distance)
    return distances


def format_distances(distances, names):
    out = []
    for di, li in zip(distances, names):
        for dj, lj in zip(di, names):
            out.append(
                f"(= (distance {li} {lj}) {dj})    (= (distance {lj} {li}) {dj})"
            )
    return out


def format_caminhos(names):
    out = []
    for name in names:
        out.append(f"(region {name})")

    return out


def euclidean_distance(A, B):
    return math.sqrt((B.x - A.x) ** 2 + (B.y - A.y) ** 2)


def get_regions(missao_json):
    regions = []
    for step in missao_json["mission_execution"]:
        regions.append(step["instructions"]["area"]["name"])
    return regions


def get_bases(mapa_json):
    bases = []
    for base in mapa_json["bases"]:
        bases.append(base["name"])
    return bases


def get_objectives(missao_json, command="", sufix=""):
    obj = []
    for step in missao_json["mission_execution"]:
        if step["command"] == command:
            obj.append(step["instructions"]["area"]["name"] + sufix)
    return obj


def list_to_str(
    l,
    prefix="",
    sufix=" ",
    diff=False,
    first_prefix="",
    first_sufix="",
    last_prefix="",
    last_sufix="",
):
    s = ""
    for i, item in enumerate(l):
        if diff:
            if i == 0:  # first
                s += first_prefix + item + first_sufix
            elif i == len(l) - 1:  # last
                s += last_prefix + item + last_sufix
            else:
                s += prefix + item + sufix
        else:
            s += prefix + item + sufix

    return s


def list_to_geopoint(l):
    return GeoPoint(l[0], l[1], l[2])


def read_json(mission, mapa):

    regions = []
    names = []
    labels = []

    geo_home = list_to_geopoint(mapa["geo_home"])

    for miss in mission["mission_execution"]:
        step = miss["instructions"]["area"]

        geo_points = [list_to_geopoint(gp) for gp in step["geo_points"]]
        cart_points = [geo_to_cart(gp, geo_home) for gp in geo_points]
        geo_center = list_to_geopoint(step["center"])
        cart_center = geo_to_cart(geo_center, geo_home)

        names.append(step["name"])

        region = Region(
            step["name"], step["name"], geo_points, cart_points, geo_center, cart_center
        )

        regions.append(region)
        labels.append(miss["command"])

    for base in mapa["bases"]:

        geo_points = [list_to_geopoint(gp) for gp in base["geo_points"]]
        cart_points = [geo_to_cart(gp, geo_home) for gp in geo_points]
        geo_center = list_to_geopoint(base["center"])
        cart_center = geo_to_cart(geo_center, geo_home)

        names.append(base["name"])

        region = Region(
            base["id"], base["name"], geo_points, cart_points, geo_center, cart_center
        )

        regions.append(region)
        labels.append("base")

    return regions, names, labels, geo_home
