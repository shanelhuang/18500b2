
from enum import Enum
from PIL import Image
import constants
from pgm_utils import pgm_save
import io

class MapData(Enum):
	'''
	Custom encoding for internal data storage.
	'''

	NULL = 0
	WALL = 1
	ROBOT = 2
	DESTINATION = 3


class Map:
	'''
	Central data type handling navigation. Stores both raw map and processed
	map. Handles most of the path planning.
	'''

	# attributes
	byte_map = bytearray(constants.MAP_SIZE * constants.MAP_SIZE)
	compressed_map = bytearray(constants.NUM_CHUNKS * constants.NUM_CHUNKS)
	data_map = bytearray(constants.MAP_SIZE * constants.MAP_SIZE)

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

	def printCompressedMap(self):
		'''
		Save compressed_map to a .pgm file in the /resources folder.
		'''
		pgm_save('../resources/compressed_map.pgm', self.compressed_map, (constants.NUM_CHUNKS, constants.NUM_CHUNKS))


	def printOverlayMap(self):
		'''
		Overlay data_map on compressed_map in color, and save to a .png file.
		'''

		im = Image.open(io.BytesIO(self.byte_map))
		im.save('../resources/overlay_map.png')
		#Image.open('../resources/compressed_map.pgm').save('../resources/overlay_map.png')
























