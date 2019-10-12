# Geo to WP converter

Algorithm to convert a file to another considering a set of rules.
The main point is to convert .csv to .wp


## Usage
Examples:

```
python3 convertion.py -i input/in_2.txt -o output/out_2_generated.wp -a 13 -c cart_to_geo -g input/geo_home_example.json
```


### Parameters

`-i` REQUIRED input path to file containing latitude, longitude and altitude values ex: `input/in_2.txt`

`-o` REQUIRED output path to save file, either inform a path containing the extension or inform the extension by using the -e parameter. ex: `output/out_2_generated.wp`

`-e` OPTIONAL extension format to output the file (standard is wp). ex: `svg`

`-a` OPTIONAL if this information is not in the input file, you can manually set the maximum altitude. ex: `13`

`-s` OPTIONAL quantity of header rows to skip. ex: `1`

`-c` OPTIONAL a flag to inform what type of conversion will be made, if convertion between cartesian and geographical point is necessary. Options: `cart_to_geo`, `geo_to_cart`

`-g` OPTIONAL the file containing the geo_home for referencing. Information about the 0,0 point in the cartesian plane, necessary to pass a geo point informing where the home is. This parameter can be informed in many ways:
* (1) pass a json element. ex: `{"latitude":000, "longitude":000, "altitude":000}`
* (2) pass a path to a json file containing the same structure as mentioned before. ex: `input/geo_home.json`
* <s>(3) a flag informing to take the first line of the file</s>(not yet supported)


## Files

### Input
Supported input formats: .csv  .txt  <s>.kml</s>(not yet supported)


### Output
Supported output formats: .wp  <s>.sgl</s>(not yet supported)


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
