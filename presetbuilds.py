from pathplanning import Drone


# Drone constructor

# Drone Mavic Pro model I
def build_drone_MavicProI()
    return Drone(743.0, 10.0, 18.9, 65.0, 32.5)

# Drone Phantom 4 model Pro V2
def build_drone_Phatom4ProV2()
    return Drone(1375.0, 10.0, 21.0, 72.0, 36.0)

# Drone Phantom 4 model Pro
def build_drone_Phatom4Pro()
    return Drone(1388.0, 10.0, 21.0, 72.0, 36.0)

# Drone Phantom 4 model Advanced
def build_drone_Phatom4Advanced()
    return Drone(1368.0, 10.0, 21.0, 72.0, 36.0)



# Camera constructor

# Mavic Pro model I
def build_camera_MavicProI():
    #return camera(59.1, 78.8,3000.0, 4000.0, 1, 1.0 / 8000.0, 12.0, 5.0, 200.0)
    return camera(78.8, 59.1, 4000.0, 3000.0, 1, 1.0 / 8000.0, 12.0, 5.0, 200.0, 6.17, 4.5, 28.0)

'''
public static Cam buildGoPro7() {
//        return new Cam(78.8, 59.1, 4000.0, 3000.0, 1, 1.0 / 8000.0, 12.0, 15.0, 455.00);
//    }
'''


# Area constructor

# Jardim Senai
def build_area_jardimSenai():
	return Area(
        GeoPoint(-48.45255874975791, -27.43338368181769, 0),
        GeoPoint(-48.45257490160673, -27.43336038312699, 1),
        GeoPoint(-48.45235131274588, -27.43329678596995, 1),
        GeoPoint(-48.45239011279272, -27.43319913253362, 4),
        GeoPoint(-48.45261463110952, -27.43325291267052, 4)
    );