import argparse
import collections
import re
import json

from fastkml import kml
import pandas as pd

from utils import GeoPoint, CartesianPoint, transform_geo_points

#GeoPoint = collections.namedtuple('GeoPoint', 'latitude, longitude, altitude')
#CartesianPoint = collections.namedtuple('CartesianPoint', 'x, y, z')


def main():
    parser = argparse.ArgumentParser()

    #Input file    
    parser.add_argument('-i',
                        '--input_filename',
                        required=True,
                        help='input path to file containing lat, long and alt values')

    #Output path   
    parser.add_argument('-o',
                        '--output_filename',
                        required=True,
                        help='output path to save file')

    #Output file extension
    parser.add_argument('-e',
                        '--output_extension',
                        default = 'wp',
                        required=False,
                        help='extension format to output the file (standard is .wp)'
    )

    #Altitude information
    parser.add_argument('-a',
                        '--altitude',
                        required=False,
                        help='If this information is not in the input file, you can manually set the maximum altitude'
    )

    #Quantity of header rows to skip
    parser.add_argument('-s',
                        '--skiprows',
                        default=0,
                        required=False,
                        help='Quantity of header rows to skip'
    )

    #A flag to inform what type of conversion will be made
    parser.add_argument('-c',
                        '--convert',
                        required=False,
                        help='If convertion between cartesian and geographical point is necessary. Options: cart_to_geo, geo_to_cart'
    )

    # The file containing the geo_home for referencing
    parser.add_argument('-g',
                        '--geo_home',
                        required=False,
                        help='information about the 0,0 point in the cartesian plane, necessary to pass a geo point informing where the home is. \
                            This parameter can be informed in many ways: \
                            (1) pass a json element. ex: {"latitude":000, "longitude":000, "altitude":000}\
                            (2) pass a path to a json file containing the same structure as mentioned before. ex: input/geo_home.json'
                            #(3) a flag informing to take the first line of the file'
    )
    # -- until here, on the readme


    try:

        args = parser.parse_args()
        execute(args)

    except Exception as e:
       print(e)
       print('Exiting...')
       exit()


def execute(args):
    input_filename = args.input_filename
    output_filename = args.output_filename
    output_extension = args.output_extension


    # Read INPUT parameters
    input_extension = re.sub(r'([A-Za-z0-9_/ ]+\.{1})', '', input_filename)
    read_options = {
        'csv': read_csv,
        'txt': read_txt,
        'kml': read_kml
    }
    assert read_options[input_extension], 'Unsupported INPUT file extension!\n(INPUT supports only: .csv .txt .kml)'


    # Read OUTPUT parameters
    if not output_extension:
        output_extension = re.sub(r'([A-Za-z0-9_/ ]+\.{1})', '', output_filename)
    output_extension = re.sub(r'\.', '', output_extension)
    write_options = {
        'sgl': write_sgl,
        'wp': write_wp
    }
    assert write_options[output_extension], 'Unsupported OUTPUT file extension!\n(OUTPUT supports only: .sgl .wp)'

    # Read other parameters
    if args.convert:
        if args.convert == 'geo_to_cart':
            print('!!! Function under construction !!!')

        elif args.convert == 'cart_to_geo':
            point = CartesianPoint

            # Read input file
            route = read_options[input_extension](input_filename, point, args)

            geo_home = read_geo_home(args)
            geo_route = transform_geo_points(route, geo_home)


    # Write output file
    output_filename = re.sub(r'(\.{1}.{1,4}$)', '', output_filename)
    output_filename += '.' + output_extension

    

    if write_options[output_extension](output_filename, geo_route):
        print("\n\nSaved file sucessfully!\nFile generated: {}".format(output_filename))
    else:
        print("Something went wrong...\nExiting...")



# READ
# --------------------------------------------------------------------------
def read_csv(filename, point, args):
    df = pd.read_csv(filename, skiprows=int(args.skiprows))
    route = []

    for _, row in df.iterrows():
        #print(row)
        assert len(df.columns) == 3, "Number of columns does not match. Expected 3, got {}".format(len(df.columns))

        point_i = point(row[1], row[0], row[2])
        route.append(point_i)

    return route


def read_txt(filename, point, args):
    df = pd.read_csv(filename, skiprows=int(args.skiprows), sep=' ')
    route = []

    for _, row in df.iterrows():
        #print(row)
        assert len(df.columns) == 3 or len(df.columns) == 2, "Number of columns does not match. Expected 2 or 3 columns, got {}".format(len(df.columns))

        if len(df.columns) == 2:
            assert args.altitude, "Information about altitude is not present in the file neither provided by user"
            point_i = point(row[0], row[1], float(args.altitude))

        elif len(df.columns) == 3:
            point_i = point(row[0], row[1], row[2])


        route.append(point_i)

    return route


def read_kml(filename, point, args):
    #print('!!! Function under construction !!!')

    with open(filename, 'rt', encoding="utf-8") as file:
        doc = file.read()
        k = kml.KML()
        k.from_string(doc)
        print(k.to_string(prettyprint=True))

    return False


def read_geo_home(args):
    flag = args.geo_home
    if re.search(r'(.json)',flag):
        with open(flag, 'r') as file:
            json_file = json.load(file)

    else:
        json_file = json.load(flag)

    geo_home = GeoPoint(json_file['latitude'], json_file['longitude'], json_file['altitude'])

    return geo_home



# WRITE
# --------------------------------------------------------------------------
def write_sgl(filename, geo_route):
    with open(filename, 'w+') as file:
        current_waypoint = 1

        file.write('<number of polygons>\n')
        file.write(number_of_polygons + '\n')
		file.write('<number of zona n>\n')
        file.write(number_of_zona_n + '\n')
		file.write('<number of zona p>\n')
        file.write(number_of_zona_p + '\n')
		file.write('<number of zona b>\n')
        file.write(number_of_zona_b + '\n')

        def write_sgl_points(points, zone_type):
        	for i, point in enumerate(points):
        		file.write('<x..., y..., n = {}, id = {}, type = {}>\n'.format(?, str(i), zone_type))

        write_sgl_points(points_zona_n, 'n')
        write_sgl_points(points_zona_p, 'p')
        write_sgl_points(points_zona_b, 'b')

    return True


def write_wp(filename, geo_route):
    with open(filename, 'w+') as file:
        current_waypoint = 1

        file.write('QGC WPL 120\n') # Determines the file version

        for i, geo_point in enumerate(geo_route):
            file.write(
                str(i) + '\t'
                + str(current_waypoint) + '\t' 
                + '3\t16\t3\t0\t0\t0\t'
                + '{:10.8f}'.format(geo_point.latitude) + '\t' 
                + '{:10.8f}'.format(geo_point.longitude) + '\t'
                + '{:10.8f}'.format(geo_point.altitude) + '\t'
                + '1'
                + '\n'
            )

            current_waypoint = 0

    return True
    



if __name__=="__main__":
    main()