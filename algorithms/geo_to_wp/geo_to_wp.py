import pandas as pd
import argparse
import collections



def main():
    parser = argparse.ArgumentParser()

    #Input file    
    parser.add_argument('-i',
                        '--input_filename',
                        required=True,
                        help='input path to file containing lat, long and alt values in a CSV')

    #Output path   
    parser.add_argument('-o',
                        '--output_filename',
                        required=True,
                        help='output path to save .wp')


    #try:

    args = parser.parse_args()
    execute(args.input_filename, args.output_filename)

    #except Exception as e:
    #    print(e)


def execute(input_filename, output_filename):
    geo_route = read_file(input_filename)
        
    if save_mavros(output_filename, geo_route):
        print("\n\nSaved file sucessfully!\nFile generated: {}.wp".format(output_filename))



def read_file(filename):
    #with open(filename, 'r') as file:
    #    df = pd.read_csv(file)
    df = pd.read_csv(filename, skiprows=1)
    geo_route = []
    geo_point = collections.namedtuple('geo_point', 'latitude, longitude, altitude')


    for i, row in df.iterrows():
        print(row)
        geo_point_i = geo_point(row[1], row[0], row[2])
        geo_route.append(geo_point_i)


    return geo_route




def save_mavros(filename, geo_route):
    with open(filename + '.wp', 'w+') as file:
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