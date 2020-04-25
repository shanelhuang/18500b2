from enum import IntEnum
import queue

# settings
MAP_SIZE = 800  # pixel size of input
CHUNK_SIZE = 10  # compression factor
MIN_SEARCH = 5  # start searching this far away
MAX_SEARCH = 20  # max chunks outward to search
NUM_CHUNKS = MAP_SIZE // CHUNK_SIZE
DEST_THRESHOLD = 150  # how unexplored constitutes a valid destination
TURN_SPEED = 100
TURN_SPEED_DEGREES = 60
SPEED = 100
MAP_SIZE_METERS = 10
CHUNK_SIZE_METRES = 1/((MAP_SIZE/MAP_SIZE_METERS)/CHUNK_SIZE)
CHUNK_MOVE_TIME = CHUNK_SIZE_METRES/(SPEED/1000)

# final map settings
FINAL_CHUNK_SIZE = 2
FINAL_NUM_CHUNKS = MAP_SIZE // FINAL_CHUNK_SIZE

# turn constants
TURN_RIGHT = 1.5
TURN_BACK = 3
TURN_LEFT = 1.5

# obstacle points threshold
POINTS_THRESHOLD = 3


# roomba conversions
# 600mm /rotation at 100mm/s


class MapData(IntEnum):
    '''
    Custom encoding for internal data storage.
    '''
    NULL = 0
    WALL = 1
    PATH = 2
    FILL = 3
    AVOID = 4
    WALL_AVOID = 5


class Heading(IntEnum):
    '''
    Encoding for robot bearing, stored as degrees from E CCW
    '''
    EAST = 0
    NORTH = 90
    WEST = 180
    SOUTH = 270
    BACK = 1000


class Status(IntEnum):
    '''
    Used for program control flow
    '''
    START = 0
    FOUND_OBSTACLE = 1
    RUNNING = 2
    END_OF_PATH = 3
    LIDAR_OBSTACLE = 5


# all the info about current program given to each thread
class ProgramInfo():
    programStatus = Status.START
    SLAMvals = [0, 0]
    directionsQueue = queue.Queue()
    foundObstacle = False
    mapbytes = bytearray(MAP_SIZE * MAP_SIZE)
    roombaPort = None
    robot_pos = [0, 0]
    dest = (1, 1)
    heading = Heading.NORTH
    obstacleLocation = [0,0,0]
    stop = False
