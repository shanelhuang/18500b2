from enum import IntEnum

# settings
MAP_SIZE = 800 # pixel size of input
CHUNK_SIZE = 10 # compression factor
MIN_SEARCH = 3 # start searching this far away
MAX_SEARCH = 10 # max chunks outward to search
SEARCH_ROW = 40 # row, col to begin the nav plan (array starts at 0)
SEARCH_COL = 35
NUM_CHUNKS = MAP_SIZE // CHUNK_SIZE
DEST_THRESHOLD = 150 # how unexplored constitutes a valid destination

# roomba conversions
# 600mm /rotation at 100mm/s


class MapData(IntEnum):
    '''
    Custom encoding for internal data storage.
    '''
    NULL = 0
    WALL = 1
    PATH = 2

class Heading(IntEnum):
	'''
	Encoding for robot bearing, stored as degrees from E CCW
	'''
	EAST = 0
	NORTH = 90
	WEST = 180
	SOUTH = 270
	