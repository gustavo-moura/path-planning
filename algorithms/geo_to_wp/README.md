# Geo to WP converter

Algorithm to convert a file to another considering a set of rules.
The main point is to convert .csv to .wp


## Usage
Examples:

```
python3 geo_to_wp.py -i input_file.csv -o output_file -s 1

python3 geo_to_wp.py -i in_2.txt -o out_2_generated.wp -a 13
```


### Parameters

`-i` REQUIRED input path to file containing lat, long and alt values

`-o` REQUIRED output path to save file, either inform a path containing the extension or inform the extension by using the -e parameter

`-e` OPTIONAL extension format to output the file (standard is wp)

`-a` OPTIONAL if this information is not in the input file, you can manually set the maximum altitude

`-s` OPTIONAL quantity of header rows to skip



## Files

### Input
Supported input formats: .csv .txt <s>.kml</s>(not yet supported)


### Output
Supported output formats: .wp <s>.sgl</s>(not yet supported)


### Examples

The CSV file should look like this:

```
"longitude", "latitude", "altitude"
-47.932749, -22.002332, 7
-47.932794, -22.002177, 13
[...]
```
OBS: be aware that the position of columns are important

The output file will look like this:

```
QGC WPL 120
0	1	3	16	3	0	0	0	-22.00217700	-47.93279400	13.00000000	1
1	0	3	16	3	0	0	0	-22.00214700	-47.93266400	13.00000000	1
[...]
```
