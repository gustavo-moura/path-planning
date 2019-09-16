# Geo to WP converter

Algorithm to convert a CSV file to a .WP in the format that the Mavros uses.


## Usage
run the line:

```
python3 main.py -i input_file.csv -o output_file
```

OBS: notice that the `-i` file must have the extension declareted and the `-o` must NOT have the extension declareted.

## Files

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
