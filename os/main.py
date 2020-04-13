import nav.map as map
import create2api
import threading
import input
import time
import nav.constants as constants
import os
import queue


if __name__ == "__main__":
	# robot initialization
	# bot = create2api.Create2()
	# bot.start()
	# bot.safe()

	# global variables
	directionsQueue = queue.Queue()

	# read user input thread
	moveThread = threading.Thread(target = input.run, args=(directionsQueue,))
	moveThread.start()


	# read in binary file
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, './resources/map.bin')

	with open(filename, "rb") as binary_file:
		bytemap = bytearray(binary_file.read())

	# create map
	map = map.Map(bytemap)
	map.compress()
	#map.printCompressedMap()
	map.findWalls()
	map.robot_pos = [40, 40]
	#map.chooseDestination()
	map.dest = [40, 60]
	directions = map.getPath()

	for step in directions:
		directionsQueue.put(step)

	map.printOverlayMap()
