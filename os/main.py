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
from rplidar import RPLidar as Lidar


if __name__ == "__main__":

    currentProgram = constants.ProgramInfo()

    # slam thread
    slamThread = threading.Thread(
        target=rpslam.slam, args=(currentProgram,))
    slamThread.daemon = True
    slamThread.start()

    # robot initialization
    while (not currentProgram.roombaPort): pass
    bot = create2api.Create2(currentProgram.roombaPort)
    bot.start()
    bot.safe()
    bot.full()

    # move robot thread
    moveThread = threading.Thread(target=move.run, args=(currentProgram, bot))
    moveThread.daemon = True
    moveThread.start()

    # obstacle thread
    obstacleThread = threading.Thread(
        target=sensors.monitor, args=(currentProgram, bot))
    obstacleThread.daemon = True
    # obstacleThread.start()

    # read in binary file
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './resources/map.bin')

    with open(filename, "rb") as binary_file:
    	bytemap = bytearray(binary_file.read())

    # create map
    while True:
        try: 
            if (currentProgram.programStatus == constants.Status.START or
                currentProgram.programStatus == constants.Status.FOUND_OBSTACLE or
                    currentProgram.programStatus == constants.Status.END_OF_PATH):
                # currMap = map.Map(currentProgram.mapbytes)
                currMap = map.Map(bytemap)
                currMap.compress()
                # map.printCompressedMap()
                currMap.findWalls()
                # currMap.chooseDestination()
                currMap.robot_pos = [40,40]
                currMap.dest = [41,41]
                directions = currMap.getPath()
                for step in directions:
                    currentProgram.directionsQueue.put(step)

            # gracefully shut down
            elif (currentProgram.programStatus == constants.Status.STOP):
                currMap.printOverlayMap()
                bot.drive_straight(0)
                moveThread.join()
                slamThread.join()
                # obstacleThread.join()
                exit(0)

        except KeyboardInterrupt:
            currentProgram.programStatus = constants.Status.STOP




