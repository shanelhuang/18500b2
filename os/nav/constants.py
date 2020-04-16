from enum import IntEnum
import queue

# settings
MAP_SIZE = 800  # pixel size of input
CHUNK_SIZE = 10  # compression factor
MIN_SEARCH = 3  # start searching this far away
MAX_SEARCH = 10  # max chunks outward to search
NUM_CHUNKS = MAP_SIZE // CHUNK_SIZE
DEST_THRESHOLD = 150  # how unexplored constitutes a valid destination
TURN_SPEED = 100
TURN_SPEED_DEGREES = 60
SPEED = 200
MAP_SIZE_METERS = 10

# turn constants
TURN_RIGHT = 1.5
TURN_BACK = 3
TURN_LEFT = 1.5

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


class Status(IntEnum):
    '''
    Used for program control flow
    '''
    START = 0
    FOUND_OBSTACLE = 1
    RUNNING = 2
    END_OF_PATH = 3
    STOP = 4


# all the info about current program given to each thread
class ProgramInfo():
    programStatus = Status.START
    SLAMvals = [0, 0]
    directionsQueue = queue.Queue()
    foundObstacle = False
    mapbytes = bytearray(MAP_SIZE * MAP_SIZE)
