

# --------------- Preset Builds


# --------------- Classes


class Map()

	def __init__(self, bonificadoras, penalizadoras, nao_navegaveis):
		self.bonificadoras = bonificadoras
		self.penalizadoras = penalizadoras
		self.nao_navegaveis = nao_navegaveis


class GeoPoint():

    #def __init__(self, longitude, latitude, height):   
        # self.longitude = longitude
        # self.latitude = latitude
        # self.height = height
    def __init__(self, tupler):
        self.longitude = tupler[0]
        self.latitude = tupler[1]
        self.height = tupler[2]
		