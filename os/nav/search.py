import constants
import numpy as np


class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


"""
Implementation of A* pathfinding algorithm
Uses manahattan distance heuristic
Returns list of tuples as a path from start to destination
"""


def astar(maze, start, end):
    # create start/end nodes, open/closed lists
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open = []
    closed = []

    open.append(start_node)
    while len(open) > 0:
        # get current node
        current_node = open[0]
        current_index = 0
        for index, item in enumerate(open):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open.pop(current_index)
        closed.append(current_node)

        # Found the goal
        if (current_node.position[0] == end_node.position[0]) and (current_node.position[1] == end_node.position[1]):
            print("here")
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure in range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue
            # Make sure not a wall
            if maze[node_position[0]][node_position[1]] == constants.MapData.WALL:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # add children only if not in closed and open
        for child in children:
            # check if child is in closed list
            add = True
            for closed_child in closed:
                if (child.position[0] == closed_child.position[0]) and (child.position[1] == closed_child.position[1]):
                    add = False

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # check if child is in the open list
            for open_node in open:
                if (child.position[0] == open_node.position[0]) and (child.position[1] == open_node.position[1]):
                    # and child.g >= open_node.g
                    add = False

            if (add):
                open.append(child)
