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
import sys


if __name__ == "__main__":
    sys.setrecursionlimit(3000)
    currentProgram = constants.ProgramInfo()
    currMap = map.Map()

    #

    # slam thread
    slamThread = threading.Thread(
        target=rpslam.slam, args=(currentProgram,))
    slamThread.daemon = True
    slamThread.start()


    # robot initialization
    while (not currentProgram.roombaPort):
        pass
    bot = create2api.Create2(currentProgram.roombaPort)
    bot.start()
    bot.safe()
    bot.full()

    print("intitializing")
    time.sleep(2)
    print("intitialized")

    # move robot thread
    moveThread = threading.Thread(
    target=move.run, args=(currentProgram, bot))
    moveThread.daemon = True
    moveThread.start()

    # obstacle thread
    obstacleThread = threading.Thread(
        target=sensors.monitor, args=(currentProgram, currMap, bot))
    obstacleThread.daemon = True
    obstacleThread.start()

    # read in binary file
    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, './resources/map.bin')

    # with open(filename, "rb") as binary_file:
    #     bytemap = bytearray(binary_file.read())

    # create map
    while True:
        try:
            # gracefully shut down
            if (currentProgram.stop):
                currMap.getPath(
                    currentProgram.robot_pos, currentProgram.dest)
                currMap.printOverlayMap(
                    currentProgram.robot_pos, currentProgram.dest)
                currMap.finalCompress()
                currMap.printUserMap()
                bot.drive_straight(0)
                print("joing threads -")
                obstacleThread.join()
                print("obstacle join")
                moveThread.join()
                print("move join")
                slamThread.join()
                print("slam join")
                exit(0)

            if ((currentProgram.programStatus == constants.Status.FOUND_OBSTACLE) or 
            (currentProgram.programStatus == constants.Status.FOUND_OBSTACLE)):
                pass
            elif (currentProgram.programStatus == constants.Status.START or
                    currentProgram.programStatus == constants.Status.END_OF_PATH):

                currMap.byte_map = currentProgram.mapbytes
                currMap.compress()
                # map.printCompressedMap()
                currMap.findWalls()
                if (currMap.checkForCompletion(currentProgram.robot_pos) == True):
                # if False:
                    currentProgram.stop = True
                    # pass
                else:
                    directions, badDestList = [], []
                    while (len(directions) == 0):
                        currentProgram.dest = currMap.chooseDestination(
                            currentProgram.robot_pos, badDestList)
                        print(currentProgram.dest)
                        directions = currMap.getPath(
                            currentProgram.robot_pos, currentProgram.dest)
                        if (len(directions) == 0):
                            badDestList.append(currentProgram.dest)
                            print("appended")
                    badDestList.append(currentProgram.dest)
                    for step in directions:
                        currentProgram.directionsQueue.put(step)
                    # currMap.printOverlayMap(
                    #     currentProgram.robot_pos, currentProgram.dest)


        except KeyboardInterrupt:
            currentProgram.stop = True