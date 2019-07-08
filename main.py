# cd /mnt/c/Projetos/path-planning
import pandas as pd

# import argparse
import sys

# import pathplanning as pp 

obj_parameters = {
        'drone': ['name', 'weight', 'min_battery', 'max_battery', 'max_velocity', 'efficient_velocity'],
        'camera': ['name', 'open_angle', 'resolution', 'max_zoom', 'shutter_time', 'mega_pixel', 'trigger', 'weight', 'sensor', 'focus_distance'],
        'area': ['name', 'geo_home', 'geo_points']
    }


def main():
    args = sys.argv
    print(args)

    iter_args = iter(args)

    for arg in iter_args:
        if arg == '--new':
            value = next(iter_args)

            res = []
            for obj in obj_parameters[value]:
                res.append(input(obj+": "))

        if arg == '--pathplanning':
            run_pathplanning()



    load_presets()




# Action Functions
# ___________________________________________________________________________

def run_pathplanning():

mission = Mission(VERTICAL_DIRECTION, UP_MOVEMENT,
                Drone.buildMavicProI(), Cam.buildMavicProI(), 
                Area.buildMiniJardimSENAITeste(), 16, 5, 1, 0.5, 0.5)

controladorGeral = Controller(mission)
controladorGeral.calcRoute()




# Support functions
# ___________________________________________________________________________

def save_to_csv(obj, data):
    print('saving'+obj)
    df = pd.DataFrame()

    filename = 'database/' + obj + 's.csv'

    with open(filename, 'r') as file:
        df = pd.read_csv(file, index_col=0)

    df = df.append(data, ignore_index=True)

    print(df)
    with open(filename, 'w') as file:
        df.to_csv(file)


def add(obj, values):
    d = {}

    

    keys = obj_parameters[obj]

    for key, value in zip(keys, values):
        d[key] = value

    return d


def load_presets():
    
    drones = [
        ['MavicProI', 743.0, 10.0, 18.9, 65.0, 32.5],
        ['Phatom4ProV2', 1375.0, 10.0, 21.0, 72.0, 36.0],
        ['Phatom4Pro', 1388.0, 10.0, 21.0, 72.0, 36.0],
        ['Phatom4Advanced', 1368.0, 10.0, 21.0, 72.0, 36.0]
    ]

    camera = [
        ['MavicProI', (78.8, 59.1), (4000.0, 3000.0), 1, 1.0 / 8000.0, 12.0, 5.0, 200.0, (6.17, 4.5), 28.0]
    ]

    area = [
        [
            'Jardim Senai'
            (-48.45255874975791, -27.43338368181769, 0),
            (
                (-48.45257490160673, -27.43336038312699, 1),
                (-48.45235131274588, -27.43329678596995, 1),
                (-48.45239011279272, -27.43319913253362, 4),
                (-48.45261463110952, -27.43325291267052, 4)
            )
        ]
    ]


    for model in drones:
        save_to_csv('drone', add('drone', model))

    for model in camera:
        save_to_csv('camera', add('camera', model))

    for model in area:
        save_to_csv('area', add('area', model))





main()


















