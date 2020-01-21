import itertools

from genetic.file_manipulation import read_mapa, write_mavros
from genetic.data_definitions import GeoPoint, CartesianPoint, Conversor, Mapa
from genetic.genetic import Genetic, Subject
from genetic.visualization import plot_map


par_RC = {
    "max_exec_time": 180,
    "C_d": 1000,
    "C_obs": 4000,
    "C_con": 0,
    "C_cur": 0,
    "C_t": 0,
    "C_dist": 1,
    "v_min": -3.0,
    "v_max": 3.0,
    "T_min": 5,
    "T_max": 20,
    "a_min": -1.0,
    "a_max": 1.0,
    "e_min": -3,
    "e_max": 3,
    "min_precision": 0.1,
    "gps_imprecision": 0,
    "population_size": 40,
    "taxa_cross": 2,
    "mutation_prob": 0.7,
}


def run_genetic(**kwargs):
    # ENTRADA

    # Parâmetros recebidos (arquivo .srv)
    origin_lat = kwargs["origin_lat"]
    origin_long = kwargs["origin_long"]
    origin_alt = kwargs["origin_alt"]
    destination_lat = kwargs["destination_lat"]
    destination_long = kwargs["destination_long"]
    destination_alt = kwargs["destination_alt"]
    map_id = kwargs["map_id"]

    print(origin_lat)

    # Leitura do arquivo declarando o MAPA em json
    # PATH = "/home/vannini/drone_arch/Data/mapa.json"  # Ubuntu Veronica
    PATH = "./data/mapa.json"  # Local


    geo_home, areas_b, areas_p, areas_n = read_mapa(PATH, map_id)
    # geo_home, _, _, areas_n = upload_mapa(mapa_file, mapa_id)

    cart_origin = Conversor.geo_to_cart(
        GeoPoint(origin_lat, origin_long, origin_alt), geo_home
    )
    cart_destination = Conversor.geo_to_cart(
        GeoPoint(destination_lat, destination_long, destination_alt), geo_home
    )

    mapa = Mapa(cart_origin, cart_destination, areas_n, inflation_rate=3)

    # EXECUÇÃO DO AG
    ag_teste = Genetic(Subject, mapa, px0=cart_origin.x, py0=cart_origin.y, **par_RC)

    best = ag_teste.run(info=True)

    # Melhor rota encontrada : WPs em cartesiano
    cart_points = best.get_route()

    # Melhor rota encontrada : WPs em geográfico
    geo_points = [
        Conversor.cart_to_geo(CartesianPoint(cart_point[0], cart_point[1]), geo_home)
        for cart_point in cart_points
    ]

    # Visualização do Mapa usado, com a rota do melhor de todos
    areas = [area for area in itertools.chain(mapa.areas_n, mapa.areas_n_inf)]
    tipos = ["n" for _ in range(len(areas))]
    plot_map(
        areas=areas,  # Mapa usado
        labels=tipos,  # Tipo do mapa {'n','p','b'} <- Não afeta o genético, só muda a visualização
        origem=mapa.origin,  # waypoint de origem
        destino=mapa.destination,  # waypoint de destino
        waypoints=best.get_route(),  # rota do melhor de todos
    )

    # SAÍDA

    # /Interface Gráfica

    # output_filename = "/home/vannini/drone_arch/Missions/path_from_ga_output.waypoints"  # Ubuntu Veronica
    output_filename = "./path_from_ga_output.waypoints"  # Local
    write_mavros(output_filename, geo_points)

    return output_filename
