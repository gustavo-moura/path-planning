# Versão do Algoritmo Genético: v2_3

import rospy

#from visualization import plot_map, plot_stats
from genetic_v2_3 import Subject, Genetic, Mapa, Gene, GeneDecoded, CartesianPoint


def build_sample_map():
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
	
	ag = Genetic(Subject, mapa1,
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

	return best.get_route()


def genetic_server():
	rospy.init_node('genetic_server')
	s = rospy.Service('genetic', AddTwoInts, run_genetic)
	print "Running Genetic Algorithm to Path-Planning"
	rospy.spin()


if __name__ == "__main__":
    genetic_server()