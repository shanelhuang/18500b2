import create2api
import threading
import nav.constants as constants
import time


def run(currentProgram, bot):
    heading = constants.Heading.NORTH
    print('move thread')
    while True:
        if(currentProgram.directionsQueue.qsize() > 0):
            cmd = currentProgram.directionsQueue.get()
            print(cmd)
            if(heading == cmd):
                print('straight')
                # straight
                bot.drive_straight(constants.SPEED)
                currentProgram.SLAMvals[0] = constants.SPEED
                currentProgram.SLAMvals[1] = 0

            elif(abs(heading - cmd) == 180):
                print('backward')
                # backwards
                bot.turn_counter_clockwise(constants.TURN_SPEED)
                currentProgram.SLAMvals[0] = 0
                currentProgram.SLAMvals[1] = -constants.TURN_SPEED_DEGREES
                time.sleep(constants.TURN_BACK)
                bot.drive_straight(constants.SPEED)
                currentProgram.SLAMvals[0] = constants.SPEED
                currentProgram.SLAMvals[1] = 0
                heading = (heading + 180) % 360

            elif(heading - cmd == -90 or heading - cmd == 270):
                print('left')
                # turn 90 left and drive
                bot.turn_counter_clockwise(constants.TURN_SPEED)
                currentProgram.SLAMvals[0] = 0
                currentProgram.SLAMvals[1] = -constants.TURN_SPEED_DEGREES
                time.sleep(constants.TURN_LEFT)
                bot.drive_straight(constants.SPEED)
                currentProgram.SLAMvals[0] = constants.SPEED
                currentProgram.SLAMvals[1] = 0
                heading = (heading + 90) % 360

            elif(heading - cmd == 90 or heading - cmd == -270):
                print('right')
                # turn 90 right and drive
                bot.turn_clockwise(constants.TURN_SPEED)
                currentProgram.SLAMvals[0] = 0
                currentProgram.SLAMvals[1] = constants.TURN_SPEED_DEGREES
                time.sleep(constants.TURN_RIGHT)
                bot.drive_straight(constants.SPEED)
                currentProgram.SLAMvals[0] = constants.SPEED
                currentProgram.SLAMvals[1] = 0
                heading = (heading + 270) % 360
