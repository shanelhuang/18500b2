import nav.map as map
import create2api
import threading
import move
import time
import nav.constants as constants
import os
import queue
import rpslam
import sensors
from nav.constants import MAP_SIZE_METERS as MAP_SIZE_METERS
from nav.constants import MAP_SIZE as MAP_SIZE_PIXELS




if __name__ == "__main__":
	# robot initialization
	bot = create2api.Create2()
	bot.start()
	bot.safe()


	# global variables
	directionsQueue = queue.Queue()
	SLAMvals = [0,0]
	foundObstacle = [False]
	mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

	# read user input thread
	moveThread = threading.Thread(target = move.run, args=(directionsQueue,SLAMvals))
	moveThread.start()

	# slam thread 
	slamThread = threading.Thread(target = rpslam.slam, args=(SLAMvals,mapbytes))
	slamThread.start()

	#obstacle thread 
	obstacleThread = threading.Thread(target = sensors.monitor, args=(foundObstacle,))
	obstacleThread.start()

	# read in binary file
	# dirname = os.path.dirname(__file__)
	# filename = os.path.join(dirname, './resources/map.bin')

	# with open(filename, "rb") as binary_file:
	# 	bytemap = bytearray(binary_file.read())

	# create map

	while True:
		currMap = map.Map(mapbytes)
		currMap.compress()
		#map.printCompressedMap()
		currMap.findWalls()
		currMap.robot_pos = [0, 0]
		currMap.chooseDestination()
		directions = map.getPath()

		for step in directions:
		 	directionsQueue.put(step)
		 	print(step)

		# currMap.printOverlayMap()
