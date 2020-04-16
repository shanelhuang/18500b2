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

    currentProgram = constants.ProgramInfo()

    # read user input thread
    moveThread = threading.Thread(target=move.run, args=(currentProgram, bot))
    moveThread.start()

    # slam thread
    slamThread = threading.Thread(
        target=rpslam.slam, args=(currentProgram,))
    slamThread.start()

    # obstacle thread
    obstacleThread = threading.Thread(
        target=sensors.monitor, args=(currentProgram, bot))
    obstacleThread.start()

    # read in binary file
    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, './resources/map.bin')

    # with open(filename, "rb") as binary_file:
    # 	bytemap = bytearray(binary_file.read())

    # create map

    while True:
        if (currentProgram.programStatus == constants.Status.START or
            currentProgram.programStatus == constants.Status.FOUND_OBSTACLE or
                currentProgram.programStatus == constants.Status.END_OF_PATH):
            currMap = map.Map(currentProgram.mapbytes)
            currMap.compress()
            # map.printCompressedMap()
            currMap.findWalls()
            currMap.chooseDestination()
            directions = currMap.getPath()
            for step in directions:
                currentProgram.directionsQueue.put(step)
        elif (currentProgram.programStatus == constants.Status.STOP):
            currMap.printOverlayMap()
