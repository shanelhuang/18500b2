#!/usr/bin/env python3

import map
import constants
import os



# read in binary file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../resources/map.bin')

with open(filename, "rb") as binary_file:
	bytemap = bytearray(binary_file.read())

# create map
map = map.Map(bytemap)
map.compress()
#map.printCompressedMap()
map.findWalls()
map.robot_pos = [40, 40]
#map.chooseDestination()
map.dest = [40, 60]
map.getPath()

map.printOverlayMap()