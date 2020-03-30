
from enum import Enum
import constants
from pgm_utils import pgm_save

class MapData(Enum):
	NULL = 0
	WALL = 1
	ROBOT = 2
	DESTINATION = 3


class Map:

	# attributes
	byte_map = bytearray(constants.MAP_SIZE * constants.MAP_SIZE)
	compressed_map = bytearray(constants.NUM_CHUNKS * constants.NUM_CHUNKS)
	data_map = bytearray(constants.MAP_SIZE * constants.MAP_SIZE)

	def __init__(self, byte_map):
		self.byte_map = byte_map


	def compress(self):
		for chunk_row in range(constants.NUM_CHUNKS):
			for chunk_col in range(constants.NUM_CHUNKS):
				# begin current chunk
				sum = 0
				for sub_row in range(constants.CHUNK_SIZE):
					for sub_col in range(constants.CHUNK_SIZE):
						sum += self.byte_map[(chunk_row * constants.CHUNK_SIZE + sub_row) * constants.MAP_SIZE + (chunk_col * constants.CHUNK_SIZE + sub_col)]
				avg = sum // (constants.CHUNK_SIZE * constants.CHUNK_SIZE)
				self.compressed_map[(chunk_row * constants.NUM_CHUNKS) + chunk_col] = avg

	def printCompressedMap(self):
		pgm_save('../resources/compressed_map.pgm', self.compressed_map, (constants.NUM_CHUNKS, constants.NUM_CHUNKS))

