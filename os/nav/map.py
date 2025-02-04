

from PIL import Image, ImageDraw
import PIL
import nav.constants as constants
from nav.pgm_utils import pgm_save
import io
import numpy
import nav.search as search
import numpy as np


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
    final_compressed_map = [[0 for i in range(constants.FINAL_NUM_CHUNKS)]
                            for j in range(constants.FINAL_NUM_CHUNKS)]

    def __init__(self):
        pass

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

    def finalCompress(self):
        '''
        Compress the final user map just a litte bit
        '''
        for chunk_row in range(constants.FINAL_NUM_CHUNKS):
            for chunk_col in range(constants.FINAL_NUM_CHUNKS):
                # begin current chunk
                sum = 0
                for sub_row in range(constants.FINAL_CHUNK_SIZE):
                    for sub_col in range(constants.FINAL_CHUNK_SIZE):
                        sum += self.byte_map[(chunk_row * constants.FINAL_CHUNK_SIZE + sub_row) *
                                             constants.MAP_SIZE + (chunk_col * constants.FINAL_CHUNK_SIZE + sub_col)]
                avg = sum // (constants.FINAL_CHUNK_SIZE *
                              constants.FINAL_CHUNK_SIZE)
                self.final_compressed_map[chunk_row][chunk_col] = avg


    def addAvoidsAround(self,i,j):
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (i + new_position[0], j + new_position[1])
            row = node_position[0]
            col = node_position[1]
            if ( (node_position[0] >=0) and (node_position[0] < constants.NUM_CHUNKS) and (node_position[1] >=0) and (node_position[1] < constants.NUM_CHUNKS)):
                if (constants.MapData(self.data_map[row][col]) != constants.MapData.WALL):
                    self.data_map[row][col] = constants.MapData.WALL_AVOID

    def findWalls(self):
        '''
        Defines all pixels with <127 value to be a wall.
        '''
        temp = [[0 if ((constants.MapData(self.data_map[i][j]) == constants.MapData.WALL) or 
            (constants.MapData(self.data_map[i][j]) == constants.MapData.WALL_AVOID)) else 
        constants.MapData(self.data_map[i][j]) for j in range(constants.NUM_CHUNKS)]
                for i in range(constants.NUM_CHUNKS)]

        self.data_map = temp

        for i in range(constants.NUM_CHUNKS):
            for j in range(constants.NUM_CHUNKS):
                if( self.compressed_map[i][j] < 127):
                    self.data_map[i][j] = constants.MapData.WALL
                    self.addAvoidsAround(i,j)
                # if(constants.MapData(self.data_map[i][j]) == constants.MapData.AVOID):
                #     self.addAvoidsAround(i,j)

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
                    elif(datum == constants.MapData.FILL):
                        pixels[j, i] = (255, 192, 203)
                    elif(datum == constants.MapData.AVOID):
                        pixels[j, i] = (255, 165, 0)
                    elif(datum == constants.MapData.WALL_AVOID):
                        pixels[j, i] = (204, 85, 0)
                else:
                    # paint map
                    pixel = self.compressed_map[i][j]
                    pixels[j, i] = (pixel, pixel, pixel)

        # paint robot_pos and dest
        pixels[robot_pos[1], robot_pos[0]] = (255, 0, 0)
        pixels[dest[1], dest[0]] = (0, 255, 0)

        # draw scale in bottom right
        draw = ImageDraw.Draw(im)
        y1 = constants.NUM_CHUNKS * 0.9
        y2 = constants.NUM_CHUNKS * 0.9
        x2 = constants.NUM_CHUNKS * 0.9
        x1 = x1 - (constants.MAP_SIZE / constants.MAP_SIZE_METERS)
        draw.line([(x1, y1), (x2, y2)], fill = "none", width = 1)
        draw.text((x1, y1), "1 meter", font=ImageFont.load_default())


        im.save('./resources/overlay_map.png')
        # im.show()

    def printIncremental(self, robot_pos, dest, index):
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
                    elif(datum == constants.MapData.FILL):
                        pixels[j, i] = (255, 192, 203)
                    elif(datum == constants.MapData.AVOID):
                        pixels[j, i] = (255, 165, 0)
                    elif(datum == constants.MapData.WALL_AVOID):
                        pixels[j, i] = (204, 85, 0)
                else:
                    # paint map
                    pixel = self.compressed_map[i][j]
                    pixels[j, i] = (pixel, pixel, pixel)

        # paint robot_pos and dest
        pixels[robot_pos[1], robot_pos[0]] = (255, 0, 0)
        pixels[dest[1], dest[0]] = (0, 255, 0)

        # draw scale in bottom right
        draw = ImageDraw.Draw(im)
        y1 = constants.NUM_CHUNKS * 0.9
        y2 = constants.NUM_CHUNKS * 0.9
        x2 = constants.NUM_CHUNKS * 0.9
        x1 = x1 - (constants.MAP_SIZE / constants.MAP_SIZE_METERS)
        draw.line([(x1, y1), (x2, y2)], fill = "none", width = 1)
        draw.text((x1, y1), "1 meter", font=ImageFont.load_default())

        path = './resources/overlay_map_{index}.png'
        im.save(path.format(index = index))
        
        '''
        Save byte_map to a .pgm file in the /resources folder.
        '''
        path = './resources/byte_map_{index}.pgm'
        pgm_save(path.format(index = index), self.byte_map,
                 (constants.MAP_SIZE, constants.MAP_SIZE))

    def printUserMap(self):
        '''
        Overlap info on user's final_compressed_map in color, and save to a .png file.
        '''
        im = PIL.Image.new(mode="RGB", size=(
            constants.FINAL_NUM_CHUNKS, constants.FINAL_NUM_CHUNKS))
        pixels = im.load()

        for i in range(im.size[0]):
            for j in range(im.size[1]):
                datum = self.final_compressed_map[i][j]
                if(datum < 75):
                    pixels[j, i] = (0, 0, 0)
                else:
                    pixels[j, i] = (255, 255, 255)

        im.save('./resources/final_overlay_map.png')
        # im.show()

    def nextToWall(row, col):
        ''' 
        Return true if given position is next to wall in data_map
        '''
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (row + new_position[0], col + new_position[1])
            row = node_position[0]
            col = node_position[1]
            if (constants.MapData(self.data_map[row][col]) == constants.MapData.WALL) or (constants.MapData(self.data_map[row][col]) == constants.MapData.AVOID):
                return True
        return False

    def chooseDestination(self, robot_pos, badDestList):
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
                       constants.MapData(self.data_map[cur_row][cur_col]) != constants.MapData.WALL and
                       constants.MapData(self.data_map[cur_row][cur_col]) != constants.MapData.AVOID and
                       constants.MapData(self.data_map[cur_row][cur_col]) != constants.MapData.WALL_AVOID and
                       (cur_row,cur_col) not in badDestList):
                        return cur_row, cur_col
        return None

    def checkForCompletion(self, robot_pos):
        visited_map = [[0 for i in range(constants.NUM_CHUNKS)]
                       for j in range(constants.NUM_CHUNKS)]

        self.data_map[robot_pos[0]][robot_pos[1]] = constants.MapData.NULL

        data_map = self.data_map

        summed = 0
        for a in data_map:
            summed += sum(a)

        def enclosed(curr_pos, depth=0):
            depth += 1
            if (curr_pos[0] < 0 or curr_pos[0] >= constants.NUM_CHUNKS or curr_pos[1] < 0 or curr_pos[1] >= constants.NUM_CHUNKS
                    or (visited_map[curr_pos[0]][curr_pos[1]] == 1)
                    or constants.MapData(data_map[curr_pos[0]][curr_pos[1]]) == constants.MapData.WALL
                    or constants.MapData(data_map[curr_pos[0]][curr_pos[1]]) == constants.MapData.AVOID
                    or constants.MapData(data_map[curr_pos[0]][curr_pos[1]]) == constants.MapData.WALL_AVOID
                    or depth > 2950):
                return 0
            else:
                visited_map[curr_pos[0]][curr_pos[1]] = 1
                return 1 + enclosed([curr_pos[0]-1, curr_pos[1]], depth) + enclosed([curr_pos[0]+1, curr_pos[1]], depth) + enclosed([curr_pos[0], curr_pos[1]-1], depth) + enclosed([curr_pos[0], curr_pos[1]+1], depth)

        count = enclosed(robot_pos)
        print("Floodfill: ", count, "Threshold: ", constants.NUM_CHUNKS * constants.NUM_CHUNKS * 0.75)

        # for i in range(constants.NUM_CHUNKS):
        #     for j in range(constants.NUM_CHUNKS):
        #         if (visited_map[i][j] == 1):
        #             data_map[i][j] = constants.MapData.FILL

        if (count < constants.NUM_CHUNKS * constants.NUM_CHUNKS * 0.75):
            return True
        return False

    def getPath(self, robot_pos, dest):
        maze = self.data_map

        start = (robot_pos[0], robot_pos[1])
        end = (dest[0], dest[1])

        path = search.astar(maze, start, end)
        # display
        if (path is None):
            return []

        for i in range(constants.NUM_CHUNKS):
            for j in range(constants.NUM_CHUNKS):
                if (self.data_map[i][j] == constants.MapData.PATH):
                    self.data_map[i][j] = constants.MapData.NULL

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
