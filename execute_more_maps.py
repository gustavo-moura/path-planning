import re
import numpy as np
import pandas as pd
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import pickle
import itertools

from genetic.data_definitions import CartesianPoint, Mapa, Version
from genetic.visualization import plot_map, vis_mapa


from genetic.genetic import Genetic, Subject


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


def read_sgl(path, **kwargs):
    with open(path, "r") as f:
        lines = f.readlines()
        map = Mapa(
            wp_ori, wp_des, sgl_read_areas(lines), **kwargs
        )  # inflation_rate=1, mode='scalar'
    return map


def run_ags_over_path(path, show=False):
    path = str(path)
    number = re.sub(r"[A-Za-z/\-_\.]", "", path)
    print(f"1. Processing file: {number}")
    map = read_sgl(path, inflation_rate=0.1, mode="vector")

    print("1.1. Read")

    ag = Genetic(
        Subject,
        map,
        version=Version("beta", "RC"),
        # Parâmetros da classe Subject:
        px0=map.origin.x,
        py0=map.origin.y,
        **par_RC,
    )

    best = ag.run(info=False)
    print(f"2. AG generated: {number}")

    # name = re.sub(r'(\.sgl)', SUFIX+r'.png', path)
    name = EXPERIMENTS_PATH + f"mode_{MODE}_map_{str(number)}_exec_{EXEC}"

    vis_mapa(map, best.get_route(), save=name + "_best.png")

    with open(name + "_ag.p", "wb") as ag_file:
        pickle.dump(ag, ag_file)

    res = np.array([[subject.fitness, subject.birth_time] for subject in ag.ancestry])
    # name_fig, name_table, name_routes
    plot_fitness(
        res,
        map,
        ag,
        name + "_fitness.png",
        name + "_fitness2.png",
        name + "_stats.csv",
        name + "_bestall.png",
        show
    )

    print(f"2. Saved: {number}")

    return ag


def get_specific(array, birth_time_target):
    # returns index of element with closest birth time as the one provided in an array
    birth_time_specific = array[:, 1].flat[
        np.abs(array[:, 1] - birth_time_target).argmin()
    ]
    return np.where(np.isclose(array, birth_time_specific))[0][0]


def plot_fitness(np_ar, mapa, ag, name_fig, name_fig2, name_table, name_routes, show=False):
    colors = sub_colors = pl.cm.jet(np.linspace(0, 1, 7))

    plt.figure(figsize=(15, 10))
    plt.plot(np_ar[:, 1], np_ar[:, 0], color=colors[0])
    if show:
        plt.show()

    sub_routes = []
    sub_names = []
    table = []
    for a, j in enumerate([5, 10, 20, 30, 40, 50, 60]):
        index = get_specific(np_ar, j)
        point = np_ar[index]
        plt.vlines(
            point[1],
            0,
            point[0],
            color=sub_colors[a],
            linestyle="dashed",
            linewidth=1,
            alpha=0.8,
            label=str(j),
        )
        plt.hlines(
            point[0],
            0,
            point[1],
            color=sub_colors[a],
            linestyle="dashed",
            linewidth=1,
            alpha=0.8,
        )
        table.append(
            np.append(
                index,
                np.append([str(ag.ancestry[index].fitness_trace)], np.append(point, j)),
            )
        )
        plt.legend()
        sub_routes.append(ag.ancestry[index].get_route())
        sub_names.append(str(j))

    plt.savefig(name_fig)
    if show:
        plt.show()

    table = pd.DataFrame(table)
    table.columns = [
        "Individual #",
        "Fitness Trace [d, obs, con, cur, t]",
        "Fitness",
        "Real Birth Time",
        "Margin Birth Time",
    ]
    aux_table = table.iloc[:, ::-1].round(2)
    aux_table.to_csv(name_table)

    plt.figure()
    plt.plot(table["Margin Birth Time"], table["Fitness"])
    plt.xlabel("Margin Birth Time")
    plt.ylabel("Fitness")
    plt.savefig(name_fig2)
    if show:
        plt.show()

    # Visualização das melhores rotas a cada tanto tempo
    areas = [area for area in itertools.chain(mapa.areas_n, mapa.areas_n_inf)]
    tipos = ["n" for _ in range(len(areas))]
    plot_map(
        areas=areas,  # Mapa usado
        labels=tipos,  # Tipo do mapa {'n','p','b'} <- Não afeta o genético, só muda a visualização
        origem=mapa.origin,  # waypoint de origem
        destino=mapa.destination,  # waypoint de destino
        multi_waypoints=sub_routes,  # rotas do melhores de todos
        colors=sub_colors,
        title="Melhores",
        names=sub_names,
        save=name_routes,
        figsize=(15, 15),
    )


# MAIN
# =============================================================================


MODE = "R"
EXEC = "1"


MAPS_PATH = "./maps/NonRegular/"
EXPERIMENTS_PATH = "./experiments/"

wp_ori = CartesianPoint(0, 0)
wp_des = CartesianPoint(0, -10)

par_RC = {
    "max_exec_time": 60,
    "C_d": 200,
    "C_obs": 200,  # 1000,
    "C_con": 0,  # 40,
    "C_cur": 10,  # 20,
    "C_t": 0,  # 10,
    "v_min": -3.0,
    "v_max": 3.0,
    "T_min": 5,
    "T_max": 20,
    "a_min": -1.0,
    "a_max": 1.0,
    "min_precision": 0.1,
    "gps_imprecision": 0,
    "population_size": 20,
}

# =============================================================================
# use essa célula para visualizar um mapa (sem a rota)

# mapa_name = "10"  # selecione o numero do mapa (string)

# mapa_teste = read_sgl(MAPS_PATH + mapa_name + ".sgl", inflation_rate=0.1, mode="vector")
# vis_mapa(mapa_teste)

# =============================================================================
# aqui executa o AG para um mapa apenas


# Run one map only
# informe o numero do mapa a ser rodado (use duas casa. e.g. 04, 06, 09, 25, 49)
mapa_name = "06"

ag = run_ags_over_path(MAPS_PATH + mapa_name + ".sgl", show=False)

# Como ele tem a opção de rodar muitos mapas, nãão estou printando as mensagens na tela. Sóó esperar.
# =============================================================================

history = ag.history
df = pd.DataFrame(history)
df.to_csv(f"{EXPERIMENTS_PATH}mode_{MODE}_map_{mapa_name}_exec_{EXEC}_history.csv")