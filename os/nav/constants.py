from enum import IntEnum

# settings
MAP_SIZE = 800 # pixel size of input
CHUNK_SIZE = 10 # compression factor
MIN_SEARCH = 3 # start searching this far away
MAX_SEARCH = 10 # max chunks outward to search
NUM_CHUNKS = MAP_SIZE // CHUNK_SIZE
DEST_THRESHOLD = 150 # how unexplored constitutes a valid destination
TURN_SPEED = 100
TURN_SPEED_DEGREES = 60
SPEED = 200
MAP_SIZE_METERS         = 10

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

class Turn(IntEnum):
	RIGHT = 1.5
	BACK = 3 
	LEFT = 1.5

	