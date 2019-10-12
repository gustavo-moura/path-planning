# cd /mnt/c/Projetos/path-planning/genetic_algorithm
from utils import controller
from algorithms.genetic_algorithm import genetic
from algorithms.genetic_algorithm import presets

def main():
	mapa = presets.build_map_C2()

	AG = genetic.GeneticAlgorithm(genetic.Subject, mapa, verbose=True, plot=True)
	AG.run()


	omega = AG.best.get_omega()
	geo_omega = controller.transform_geo_points(omega, mapa.geo_home)


	print("\nSaving litchi file")
	AG.save_litchi([geo_omega])
	print("... done")

	print("\nSaving KML file")
	AG.save_kml([geo_omega], mapa.geo_home, mapa.get_geo_points())
	print("... done")

	print("\nEND")




if __name__ == "__main__":
	main()