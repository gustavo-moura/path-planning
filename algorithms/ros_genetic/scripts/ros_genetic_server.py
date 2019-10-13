# Versão do Algoritmo Genético: v2_3

import rospy

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


def run_genetic():
	
	## ENTRADA

	#mapa = build_sample_map()

	# TODO: Receber essas três variáveis como parâmetros na chamada do ROS node
	missao_filename = 'C:\\Projetos\\path-planning\\data\\missao.json'
	missao_id=0
	mapa_filename = 'C:\\Projetos\\path-planning\\data\\mapa.json'
	mapa, geo_home = read_mission(missao_filename, missao_id, mapa_filename)


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
	cart_points = best.get_route()


	## SAÍDA

	# TODO: Receber variável output_filename como parâmetro na chamada do ROS node
	output_filename = './output.wp'
	save_genetic_output(output_filename, cart_points, geo_home)


	return 


def genetic_server():
	rospy.init_node('genetic_server')
	s = rospy.Service('genetic', AddTwoInts, run_genetic)
	print "Running Genetic Algorithm to Path-Planning"
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