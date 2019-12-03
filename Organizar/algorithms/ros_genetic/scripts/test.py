
import argparse

from visualization import plot_map
from genetic_v2_3 import Subject, Genetic 
from data_definitions import Mapa, CartesianPoint, Conversor, GeoPoint

from file_manipulation import read_mapa, write_mavros

## ENTRADA

# Parâmetros recebidos (arquivo .srv)
origin_lat       = -22.002237
origin_long      = -47.932546
origin_alt       = 13
destination_lat  = -22.002674 
destination_long = -47.932608
destination_alt  = 15
mapa_id          = 0

# Leitura do arquvio em DATA
geo_home, _, _, areas_n = read_mapa('/mnt/c/Projetos/path-planning/data/mapa.json', mapa_id)

cart_origin      = Conversor.geo_to_cart(GeoPoint(origin_lat, origin_long, origin_alt), geo_home)
cart_destination = Conversor.geo_to_cart(GeoPoint(destination_lat, destination_long, destination_alt), geo_home)


mapa = Mapa(cart_origin, cart_destination, areas_n, inflation_rate=0.1)



## EXECUÇÃO DO AG

ag = Genetic(Subject, mapa,
        taxa_cross=1.0,
        population_size=80,
        C_d=1000,
        C_obs=10000,
        C_con=10,
        C_cur=0,
        C_t=0,
        max_exec_time=1,
        T_max=20,
        px0=cart_origin.x,
        py0=cart_origin.y
)

best = ag.run(info=True)

# Melhor rota encontrada : WPs em cartesiano
cart_points = best.get_route()

# Melhor rota encontrada : WPs em geográfico
geo_points = [ Conversor.cart_to_geo(CartesianPoint(cart_point[0], cart_point[1]), geo_home) for cart_point in cart_points ]


plot_map(
    mapa.areas_n_inf, 
    ['n' for _ in range(len(mapa.areas_n_inf))], 
    cart_origin, 
    cart_destination, 
    best.get_route(),
    None
)

## SAÍDA

output_filename = '/mnt/c/Projetos/path-planning/algorithms/ros_genetic/path_from_ga_output.wp'
write_mavros(output_filename, geo_points)