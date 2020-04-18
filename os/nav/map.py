

from PIL import Image
import PIL
import nav.constants as constants
from nav.pgm_utils import pgm_save
import io
import numpy
import nav.search as search


class Map:
    '''
    Central data type handling navigation. Stores both raw map and processed
    map. Handles most of the path planning.
    '''

    # attributes
    byte_map = bytearray(constants.MAP_SIZE * constants.MAP_SIZE)
    compressed_map = [[0 for i in range(constants.NUM_CHUNKS)]
                      for j in range(constants.NUM_CHUNKS)]
    data_map = [[0 for i in range(constants.NUM_CHUNKS)]
                for j in range(constants.NUM_CHUNKS)]

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
                        sum += self.byte_map[(chunk_row * constants.CHUNK_SIZE + sub_row) *
                                             constants.MAP_SIZE + (chunk_col * constants.CHUNK_SIZE + sub_col)]
                avg = sum // (constants.CHUNK_SIZE * constants.CHUNK_SIZE)
                self.compressed_map[chunk_row][chunk_col] = avg

    def findWalls(self):
        '''
        Defines all pixels with <127 value to be a wall.
        '''
        self.data_map = [[0 for i in range(constants.NUM_CHUNKS)]
                    for j in range(constants.NUM_CHUNKS)]

        for i in range(constants.NUM_CHUNKS):
            for j in range(constants.NUM_CHUNKS):
                if(self.compressed_map[i][j] < 127):
                    self.data_map[i][j] = constants.MapData.WALL

        # for i in range(40,61):
        #   print(self.data_map[40][i])

    def printCompressedMap(self):
        '''
        Save compressed_map to a .pgm file in the /resources folder.
        '''
        pgm_save('../resources/compressed_map.pgm', self.compressed_map,
                 (constants.NUM_CHUNKS, constants.NUM_CHUNKS))

    def printOverlayMap(self, robot_pos, dest):
        '''
        Overlay data_map on compressed_map in color, and save to a .png file.
        ''' 
        # print(self.data_map)
        im = PIL.Image.new(mode="RGB", size=(
            constants.NUM_CHUNKS, constants.NUM_CHUNKS))
        pixels = im.load()

        for i in range(im.size[0]):
            for j in range(im.size[1]):
                datum = constants.MapData(self.data_map[i][j])
                if(datum != constants.MapData.NULL):
                    # paint data
                    if(datum == constants.MapData.WALL):
                        # indices reversed for image
                        pixels[j, i] = (0, 0, 255)
                    elif(datum == constants.MapData.PATH):
                        pixels[j, i] = (255, 255, 0)
                else:
                    # paint map
                    pixel = self.compressed_map[i][j]
                    pixels[j, i] = (pixel, pixel, pixel)

        # paint robot_pos and dest
        pixels[robot_pos[1], robot_pos[0]] = (255, 0, 0)
        pixels[dest[1], dest[0]] = (0, 255, 0)

        im.save('./resources/overlay_map.png')
        # im.show()

    def chooseDestination(self, robot_pos):
        '''
        Performs a radially outward expanding search from current robot pos for 
        a square that fits the defined destination threshold for exploredness.
        '''

        for distance in range(constants.MIN_SEARCH, constants.MAX_SEARCH):
            for row_offset in range(-distance, distance):
                cur_row = robot_pos[0] + row_offset
                if(cur_row < 0 or cur_row >= constants.NUM_CHUNKS):
                    continue
                for col_offset in range(-distance, distance):
                    cur_col = robot_pos[1] + col_offset
                    if(cur_col < 0 or cur_col >= constants.NUM_CHUNKS):
                        continue
                    if((self.compressed_map[cur_row][cur_col] < constants.DEST_THRESHOLD) and
                       constants.MapData(self.data_map[cur_row][cur_col]) != constants.MapData.WALL):
                        self.dest = [cur_row, cur_col]
                        return cur_row, cur_col
        return None

    def getPath(self, robot_pos, dest):
        maze = self.data_map
        start = (robot_pos[0], robot_pos[1])
        end = (self.dest[0], self.dest[1])

        # print(start)
        # print(end)
        # print(maze)
        path = search.astar(maze, start, end)
        # display
        for grid in path:
            self.data_map[grid[0]][grid[1]] = constants.MapData.PATH

        directions = []
        prev_pos = None
        for step in path:
            # first entry
            if(prev_pos is None):
                prev_pos = step
                continue
            else:
                if(step[1] > prev_pos[1]):
                    directions.append(constants.Heading.EAST)
                elif(step[1] < prev_pos[1]):
                    directions.append(constants.Heading.WEST)
                elif(step[0] < prev_pos[0]):
                    directions.append(constants.Heading.NORTH)
                elif(step[0] > prev_pos[0]):
                    directions.append(constants.Heading.SOUTH)
                prev_pos = step

        return directions

