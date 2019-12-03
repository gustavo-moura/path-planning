import pathplanning as pp


# Drone constructor
# Parameters:
# 'drone': ['weight', 'min_battery', 'max_battery', 'max_velocity', 'efficient_velocity'],


# Drone Mavic Pro model I
def build_drone_MavicProI():
    return pp.Drone(743.0, 10.0, 18.9, 65.0, 32.5)

# Drone Phantom 4 model Pro V2
def build_drone_Phatom4ProV2():
    return pp.Drone(1375.0, 10.0, 21.0, 72.0, 36.0)

# Drone Phantom 4 model Pro
def build_drone_Phatom4Pro():
    return pp.Drone(1388.0, 10.0, 21.0, 72.0, 36.0)

# Drone Phantom 4 model Advanced
def build_drone_Phatom4Advanced():
    return pp.Drone(1368.0, 10.0, 21.0, 72.0, 36.0)



# Camera constructor
# Parameters:
# 'camera': ['open_angle', 'resolution', 'max_zoom', 'shutter_time', 'mega_pixel', 'trigger', 'weight', 'sensor', 'focus_distance'],


# Mavic Pro model I
def build_camera_MavicProI():
    return pp.Camera(
                (78.8, 59.1),
                (4000.0, 3000.0), 
                1, 
                1.0 / 8000.0, 
                12.0, 
                5.0, 
                200.0, 
                (6.17, 4.5), 
                28.0
            )



# Area constructor
# Parameters:
# 'area': ['geo_home', 'geo_points']

# Jardim Senai
def build_area_jardimSenai():
    geo_home = pp.GeoPoint((-48.45255874975791, -27.43338368181769, 0))
    points = [
        (-48.45257490160673, -27.43336038312699, 1), 
        (-48.45235131274588, -27.43329678596995, 1), 
        (-48.45239011279272, -27.43319913253362, 4), 
        (-48.45261463110952, -27.43325291267052, 4)
    ]
    geo_points = [pp.GeoPoint(i) for i in points]
    area = pp.Area(geo_home, geo_points)

    return area


# C2 Atrás do bloco do ICMC
def build_area_C2():
    geo_home = pp.GeoPoint((-47.932949, -22.002467, 0))

    points = [
        (-47.932749, -22.002332, 7), 
        (-47.932794, -22.002177, 13), 
        (-47.932664, -22.002147, 13), 
        (-47.932612, -22.002306, 7)
    ]

    geo_points = [pp.GeoPoint(i) for i in points]

    area = pp.Area(geo_home, geo_points)

    return area