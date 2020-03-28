#!/usr/bin/env python3

import os
from pgm_utils import pgm_save

MAP_SIZE = 800 # pixel size of input
CHUNK_SIZE = 10 # compression factor
MAX_SEARCH = 5 # max chunks outward to search
SEARCH_ROW = 40 # row, col to begin the nav plan (array starts at 0)
SEARCH_COL = 35



def search():
	for row_offset in range(-MAX_SEARCH - 1, MAX_SEARCH):
		cur_row = SEARCH_ROW + row_offset
		if(cur_row < 0 or cur_row >= num_chunks):
			continue
		for col_offset in range(-MAX_SEARCH - 1, MAX_SEARCH):
			cur_col = SEARCH_COL + col_offset
			if(cur_col < 0 or cur_col >= num_chunks):
				continue
			if(compressed_map_2d[cur_row][cur_col] > 0 and compressed_map_2d[cur_row][cur_col] < 200):
				return cur_row, cur_col
	return None






# read in binary file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../resources/map.bin')

with open(filename, "rb") as binary_file:
	bytemap = bytearray(binary_file.read())

# iterate map chunk by chunk and average pixels into one byte
num_chunks = MAP_SIZE // CHUNK_SIZE
compressed_map = bytearray(num_chunks * num_chunks)
compressed_map_2d = [[0 for x in range(num_chunks)] for x in range(num_chunks)]

for chunk_row in range(num_chunks):
	for chunk_col in range(num_chunks):
		# begin current chunk
		sum = 0
		for sub_row in range(CHUNK_SIZE):
			for sub_col in range(CHUNK_SIZE):
				sum += bytemap[(chunk_row * CHUNK_SIZE + sub_row) * MAP_SIZE + (chunk_col * CHUNK_SIZE + sub_col)]
		avg = sum // (CHUNK_SIZE * CHUNK_SIZE)
		if(avg < 127):
			avg = 0
		compressed_map[(chunk_row * num_chunks) + chunk_col] = avg
		compressed_map_2d[chunk_row][chunk_col] = avg

# approx middle pixel
compressed_map[(SEARCH_ROW) * 80 + SEARCH_COL] = 0

# expanding radial search outward from given point
outuple = search()
if(outuple is not None):
	(dest_row, dest_col) = outuple
	print(dest_row, dest_col)
	compressed_map[dest_row * num_chunks + dest_col] = 0
else:
	print("None found")




#print(compressed_map)
pgm_save('compressed_map.pgm', compressed_map, (num_chunks, num_chunks))







