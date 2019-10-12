# cd /mnt/c/Projetos/path-planning
import pandas as pd

import sys
import os

import data_definitions as data
from algorithms.square_planning.square_planning import Planning
from algorithms.square_planning.square_planning import presetsbuilds as preset

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
            print(extract_df(get('drone', 0)))

            
            #drone = presets.build_drone_MavicProI()
            drone = presets.build_drone_Phatom4Pro()
            
            camera = presets.build_camera_MavicProI()

            area = presets.build_area_C2()

            run_pathplanning(drone, camera, area)

        if arg == '--loadpresets':
            load_presets()




# Action Functions
# ___________________________________________________________________________

def run_pathplanning(drone, camera, area):

    mission = data.Mission(data.Mission.VERTICAL_DIRECTION, data.Mission.UP_MOVEMENT,
                    drone, camera, area, 16, 5, 1, 0.5, 0.5)

    controladorGeral = Planning(mission)
    controladorGeral.calc_route()
    controladorGeral.save(['kml', 'mavros'])




# Support functions
# ___________________________________________________________________________

def extract_df(df):
    for i in df:
        yield i


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


def get(obj, index):
    print('opening'+obj)
    df = pd.DataFrame()

    filename = 'database/' + obj + 's.csv'

    with open(filename, 'r') as file:
        df = pd.read_csv(file, index_col=0)

    return df.iloc[index]


def create_files():

    for obj in ['drone', 'camera', 'area']:

        filename = 'database/' + obj + 's.csv'

        # if not os.path.isfile(filename):
        #     file = open(filename, 'w+')
        # else

        with open(filename, 'w+') as file:
            df = pd.DataFrame(columns=obj_parameters[obj])
            df.to_csv(file)



def load_presets():

    create_files()

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
            'Jardim Senai',
            (-48.45255874975791, -27.43338368181769, 0),
            [
                (-48.45257490160673, -27.43336038312699, 1),
                (-48.45235131274588, -27.43329678596995, 1),
                (-48.45239011279272, -27.43319913253362, 4),
                (-48.45261463110952, -27.43325291267052, 4)
            ]
        ]
    ]


    for model in drones:
        save_to_csv('drone', add('drone', model))

    for model in camera:
        save_to_csv('camera', add('camera', model))

    for model in area:
        save_to_csv('area', add('area', model))



main()
