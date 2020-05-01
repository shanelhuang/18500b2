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
    '''
    Main/control & Navigation thread.
    '''

    print("Initializing")
    # python default is 500, set to 3k for floodfill
    sys.setrecursionlimit(3000)
    # map filename index
    index = 0
    prevTime = time.time()

    # thread data sharing
    currentProgram = constants.ProgramInfo()
    currMap = map.Map()

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
    
    print("Initialized")

    # create map
    while True:
        try:
            # print incremental map every second
            if(time.time() - prevTime >= 1):
                currMap.printIncremental(currentProgram.robot_pos, currentProgram.dest, index)
                index++
                prevTime = time.time()

            # gracefully shut down
            if (currentProgram.stop):
                currMap.getPath(
                    currentProgram.robot_pos, currentProgram.dest)
                currMap.printOverlayMap(
                    currentProgram.robot_pos, currentProgram.dest)
                currMap.finalCompress()
                currMap.printUserMap()
                bot.drive_straight(0)
                print("Joining threads:")
                obstacleThread.join()
                print("Obstacle joined")
                moveThread.join()
                print("Move joined")
                slamThread.join()
                print("Slam joined")
                exit(0)

            # do nothing while obstacle is being dealt with
            if ((currentProgram.programStatus == constants.Status.FOUND_OBSTACLE) or 
            (currentProgram.programStatus == constants.Status.FOUND_OBSTACLE)):
                pass

            # need to generate a new path
            elif (currentProgram.programStatus == constants.Status.START or
                    currentProgram.programStatus == constants.Status.END_OF_PATH):
                # retrieve and process map from slam
                currMap.byte_map = currentProgram.mapbytes
                currMap.compress()
                currMap.findWalls()
                if (currMap.checkForCompletion(currentProgram.robot_pos) == True):
                    print("Loop closed.")
                    currentProgram.stop = True
                else:
                    # generate destinations/paths until a valid one is found
                    directions, badDestList = [], []
                    while (len(directions) == 0):
                        currentProgram.dest = currMap.chooseDestination(
                            currentProgram.robot_pos, badDestList)
                        print(currentProgram.dest)
                        directions = currMap.getPath(
                            currentProgram.robot_pos, currentProgram.dest)
                        if (len(directions) == 0):
                            badDestList.append(currentProgram.dest)
                            print("Unreachable destination: ", currentProgram.dest)
                    badDestList.append(currentProgram.dest)
                    print("Destination selected: ", currentProgram.dest)
                    for step in directions:
                        currentProgram.directionsQueue.put(step)

                    # currMap.printOverlayMap(
                    #     currentProgram.robot_pos, currentProgram.dest)


        except KeyboardInterrupt:
            print("Exiting.")
            currentProgram.stop = True