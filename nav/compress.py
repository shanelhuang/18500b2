#!/usr/bin/env python3

import os
from pgm_utils import pgm_save

MAP_SIZE = 800
CHUNK_SIZE = 10

# read in binary file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../resources/map.bin')

with open(filename, "rb") as binary_file:
	bytemap = bytearray(binary_file.read())

# iterate map chunk by chunk and average pixels into one byte
num_chunks = MAP_SIZE // CHUNK_SIZE
compressed_map = bytearray(num_chunks * num_chunks)

for chunk_row in range(num_chunks):
	for chunk_col in range(num_chunks):
		# begin current chunk
		sum = 0
		for sub_row in range(CHUNK_SIZE):
			for sub_col in range(CHUNK_SIZE):
				sum += bytemap[(chunk_row * CHUNK_SIZE + sub_row) * MAP_SIZE + (chunk_col * CHUNK_SIZE + sub_col)]
		avg = sum // (CHUNK_SIZE * CHUNK_SIZE)
		compressed_map[(chunk_row * num_chunks) + chunk_col] = avg

#print(compressed_map)
pgm_save('compressed_map.pgm', compressed_map, (num_chunks, num_chunks))


