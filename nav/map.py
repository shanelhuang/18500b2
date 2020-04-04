
from enum import IntEnum
from PIL import Image
import PIL
import constants
from pgm_utils import pgm_save
import io
import numpy

class MapData(IntEnum):
	'''
	Custom encoding for internal data storage.
	'''

	NULL = 0
	WALL = 1
	# ROBOT = 2
	# DESTINATION = 3


class Map:
	'''
	Central data type handling navigation. Stores both raw map and processed
	map. Handles most of the path planning.
	'''

	# attributes
	byte_map = bytearray(constants.MAP_SIZE * constants.MAP_SIZE)
	compressed_map = bytearray(constants.NUM_CHUNKS * constants.NUM_CHUNKS)
	data_map = bytearray(constants.MAP_SIZE * constants.MAP_SIZE)
	robot_pos = [0, 0]
	dest = [1, 1]

	def __init__(self, byte_map):
		self.byte_map = byte_map


	def compress(self):
		'''
		Compresses the byte_map into compressed_map at a ratio defined in 
		constants.py.
		'''

		for chunk_row in range(constants.NUM_CHUNKS):
			for chunk_col in range(constants.NUM_CHUNKS):
				# begin current chunk
				sum = 0
				for sub_row in range(constants.CHUNK_SIZE):
					for sub_col in range(constants.CHUNK_SIZE):
						sum += self.byte_map[(chunk_row * constants.CHUNK_SIZE + sub_row) * constants.MAP_SIZE + (chunk_col * constants.CHUNK_SIZE + sub_col)]
				avg = sum // (constants.CHUNK_SIZE * constants.CHUNK_SIZE)
				self.compressed_map[(chunk_row * constants.NUM_CHUNKS) + chunk_col] = avg


	def findWalls(self):
		'''
		Defines all pixels with <127 value to be a wall.
		'''

		for i in range(constants.NUM_CHUNKS):
			for j in range(constants.NUM_CHUNKS):
				if(self.compressed_map[i * constants.NUM_CHUNKS + j] < 127):
					self.data_map[i * constants.NUM_CHUNKS + j] = int(MapData.WALL)


	def printCompressedMap(self):
		'''
		Save compressed_map to a .pgm file in the /resources folder.
		'''
		pgm_save('../resources/compressed_map.pgm', self.compressed_map, (constants.NUM_CHUNKS, constants.NUM_CHUNKS))


	def printOverlayMap(self):
		'''
		Overlay data_map on compressed_map in color, and save to a .png file.
		'''

		im = PIL.Image.new(mode = "RGB", size = (constants.NUM_CHUNKS, constants.NUM_CHUNKS))
		pixels = im.load()

		for i in range(im.size[0]):
			for j in range(im.size[1]):
				index = (i * constants.NUM_CHUNKS) + j
				datum = MapData(self.data_map[index])
				if(datum != MapData.NULL):
					# paint data
					if(datum == MapData.WALL):
						pixels[j,i] = (0,0,255)
					# elif(datum == MapData.ROBOT):
					# 	pixels[j,i] = (255,0,0)
					# elif(datum == MapData.DESTINATION):
					# 	pixels[j,i] = (0,255,0)
				else:
					# paint map
					pixel = self.compressed_map[index]
					pixels[j,i] = (pixel, pixel, pixel)

		# paint robot_pos and dest
		pixels[self.robot_pos[0], self.robot_pos[1]] = (255,0,0)
		pixels[self.dest[0], self.dest[1]] = (0,255,0)

		im.save('../resources/overlay_map.png')
		im.show()



























