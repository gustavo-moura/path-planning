import argparse
import collections
import re

import pandas as pd



geo_point = collections.namedtuple('geo_point', 'latitude, longitude, altitude')

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
                        help='output path to save file (standard extension is .wp)')

    #Output file extension
    parser.add_argument('-e',
                        '--output_extension',
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

    #try:

    args = parser.parse_args()
    execute(args)

    #except Exception as e:
    #    print(e)
    #    print('Exiting...')
    #    exit()


def execute(args):
    input_filename = args.input_filename
    output_filename = args.output_filename
    output_extension = args.output_extension


    # Read INPUT
    input_extension = re.sub(r'([A-Za-z0-9_/ ]+\.{1})', '', input_filename)
    read_options = {
        'csv': read_csv,
        'txt': read_txt,
        'kml': read_kml
    }
    assert read_options[input_extension], 'Unsupported INPUT file extension!\n(INPUT supports only: .csv .txt .kml)'


    # Read OUTPUT
    if not output_extension:
        output_extension = re.sub(r'([A-Za-z0-9_/ ]+\.{1})', '', output_filename)
    write_options = {
        'sgl': write_sgl,
        'wp': write_wp
    }
    assert write_options[output_extension], 'Unsupported OUTPUT file extension!\n(OUTPUT supports only: .sgl .wp)'


    # Read input file
    geo_route = read_options[input_extension](input_filename, args)
    

    # Write output file
    output_filename = re.sub(r'(\.{1}.{1,4}$)', '', output_filename)
    output_filename += '.' + output_extension

    if write_options[output_extension](output_filename, geo_route):
        print("\n\nSaved file sucessfully!\nFile generated: {}".format(output_filename))
    else:
        print("Something went wrong...\nExiting...")



# READ
# --------------------------------------------------------------------------
def read_csv(filename, args):
    df = pd.read_csv(filename, skiprows=args.skiprows)
    geo_route = []

    for _, row in df.iterrows():
        #print(row)
        assert len(df.columns) == 3, "Number of columns does not match. Expected 3, got {}".format(len(df.columns))

        geo_point_i = geo_point(row[1], row[0], row[2])
        geo_route.append(geo_point_i)

    return geo_route


def read_txt(filename, args):
    df = pd.read_csv(filename, skiprows=args.skiprows, sep=' ')
    geo_route = []

    for _, row in df.iterrows():
        #print(row)
        assert len(df.columns) == 3 or len(df.columns) == 2, "Number of columns does not match. Expected 2 or 3 columns, got {}".format(len(df.columns))

        if len(df.columns) == 2:
            assert args.altitude, "Information about altitude is not present in the file neither provided by user"
            geo_point_i = geo_point(row[0], row[1], float(args.altitude))

        elif len(df.columns) == 3:
            geo_point_i = geo_point(row[0], row[1], row[2])


        geo_route.append(geo_point_i)

    return geo_route


def read_kml(filename):
    print('!!! Function under construction !!!')

    return False



# WRITE
# --------------------------------------------------------------------------
def write_sgl(filename, geo_route):
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