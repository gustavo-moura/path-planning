from pathlib import Path
import re
import pickle

from genetic.data_definitions import Map, CartesianPoint, Version
from genetic.visualization import vis_mapa
from genetic.genetic import Genetic, Subject

from multiprocessing import Pool

PATH = "/home/gustavosouza/Documents/Per/path-planning/"
MAPS_PATH = PATH + "maps/NonRegular/"


def sgl_read_areas(lines):
    """From the map file definition reads each area"""

    lines = iter(lines)
    next(lines)  # <number of polygons>
    next(lines)  # 20

    areas = []

    for line in lines:
        Xs = [float(n) for n in re.sub(r"\n", "", next(lines)).split(",")]
        Ys = [float(n) for n in re.sub(r"\n", "", next(lines)).split(",")]

        areas.append([CartesianPoint(x, y) for x, y in zip(Xs, Ys)])

    return areas


def run_ags_over_path(path):
    try:
        path = str(path)
        number = re.sub(r"[A-Za-z/\-_\.]", "", path)
        print(f"1. Processing file: {number}")
        with open(path, "r") as f:
            lines = f.readlines()
            map = Map(wp_ori, wp_des, sgl_read_areas(lines), inflation_rate=0)

        print("1.1. Read")

        ag = Genetic(
            Subject,
            map,
            version=Version("beta", "RC"),
            # Parâmetros da classe Genetic:
            taxa_cross=5,
            population_size=10,
            max_exec_time=600,
            # Parâmetros da classe Subject:
            px0=map.origin.x,
            py0=map.origin.y,
            T_min=1,
            T_max=25,
            mutation_prob=0.7,
            gps_imprecision=1,
            **par_RC,
        )

        best = ag.run(info=False)
        print(f"2. AG generated: {number}")

        name = re.sub(r"(\.sgl)", r".png", path)
        vis_mapa(map, best.get_route(), save=name)

        name = re.sub(r"(\.sgl)", r"_ag.p", path)

        with open(name, "wb") as ag_file:
            pickle.dump(ag, ag_file)

        print(f"2. Saved: {number}")

        # vis_mapa(map)
        # maps.append(map)
        # print(f'File processed: {path}')
    except Exception as e:
        print(f"!!! {number} Problem occured!! {path}")
        print(e)


def run_ags_over_path_E(path):
    #     try:
    path = str(path)
    number = re.sub(r"[A-Za-z/\-_\.]", "", path)
    print(f"1. Processing file: {number}")
    with open(path, "r") as f:
        lines = f.readlines()
        map = Map(wp_ori, wp_des, sgl_read_areas(lines), inflation_rate=0)

    print("1.1. Read")

    ag = Genetic(
        Subject,
        map,
        version=Version("beta", "RC"),
        # Parâmetros da classe Genetic:
        taxa_cross=5,
        population_size=1000,
        max_exec_time=600,
        # Parâmetros da classe Subject:
        px0=map.origin.x,
        py0=map.origin.y,
        T_min=1,
        T_max=25,
        mutation_prob=0.7,
        gps_imprecision=1,
        **par_RC,
    )

    best = ag.run(info=True)
    print(f"2. AG generated: {number}")

    name = re.sub(r"(\.sgl)", r".png", path)
    vis_mapa(map, best.get_route(), save=name)

    name = re.sub(r"(\.sgl)", r"_ag.p", path)

    with open(name, "wb") as ag_file:
        pickle.dump(ag, ag_file)

    print(f"2. Saved: {number}")

    # vis_mapa(map)
    # maps.append(map)
    # print(f'File processed: {path}')


#     except Exception as e:
#         print(f'!!! {number} Problem occured!! {path}')
#         print(e)

par_RC = {
    "C_d": 10000,
    "C_obs": 10000,
    "C_con": 500,
    "C_cur": 100,
    "C_t": 100,
}

wp_ori = CartesianPoint(0, 0)
wp_des = CartesianPoint(0, -10)
run_ags_over_path_E(MAPS_PATH + "map_W20_023.sgl")
