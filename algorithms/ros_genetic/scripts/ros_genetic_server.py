# Versão do Algoritmo Genético: v2_3

import rospy
from GA_Planner.srv import *

import argparse

#from visualization import plot_map, plot_stats
from genetic_v2_3 import Subject, Genetic, Gene, GeneDecoded, 
from data_definitions import Mapa, CartesianPoint

from file_manipulation import read_mission

def build_sample_map():
	# Função para criar um mapa de teste

	wp_ori = CartesianPoint(10.0, 10.0)
	wp_des = CartesianPoint(40.0, 10.0)

	verts = [
	    (20.0,  5.0), # left,  bottom
	    (20.0, 15.5), # left,  top
	    (30.0, 15.5), # right, top
	    (30.0,  5.0), # right, bottom
	    (20.0,  5.0), # ignored
	]
	verts = [CartesianPoint(v[0], v[1]) for v in verts]

	mapa = Mapa(wp_ori, wp_des, [verts])

	return mapa


def run_genetic(req):
	
	## ENTRADA

	# Parâmetros recebidos (arquivo .srv)
	origin_lat       = req.origin_lat
	origin_long      = req.origin_long
	origin_alt       = req.origin_alt
	destination_lat  = req.destination_lat
	destination_long = req.destination_long
	destination_alt  = req.destination_alt
	missao_id        = req.mission_id

	# Leitura do arquvio em DATA
	geo_home, _, _, areas_n = read_mapa('~/Data/mapa.json', mapa_id)

	cart_origin      = geo_to_cart(GeoPoint(origin_lat, origin_long, origin_alt), geo_home)
	cart_destination = geo_to_cart(GeoPoint(destination_lat, destination_long, destination_alt), geo_home)


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
	        max_exec_time=60
	)

	best = ag.run(info=True)

	# Melhor rota encontrada : WPs em cartesiano
	cart_points = best.get_route()

	# Melhor rota encontrada : WPs em geográfico
	geo_points = [ Conversor.list_cart_to_geo(cart_points, geo_home) ]



	## SAÍDA

	output_filename = '~/Mission/path_from_ga_output.wp'
	write_mavros(output_filename, geo_points)


	return GA_PlannerResponse(output_filename)


def genetic_server():
	rospy.init_node('genetic_server')
	s = rospy.Service('genetic', GA_Planner, run_genetic)
	print ("Running Genetic Algorithm to Path-Planning")
	rospy.spin()


if __name__ == "__main__":

	# parser = argparse.ArgumentParser(description='Execute Genetic Algorithm to Path-Planning')
	# parser.add_argument('integers', metavar='N', type=int, nargs='+',
	#                     help='an integer for the accumulator')
	# parser.add_argument('--sum', dest='accumulate', action='store_const',
	#                     const=sum, default=max,
	#                     help='sum the integers (default: find the max)')

	# args = parser.parse_args()

    genetic_server()