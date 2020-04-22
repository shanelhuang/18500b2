import create2api
import threading
import nav.constants as constants
import time


# def run(currentProgram, bot):
#     while (currentProgram.programStatus != constants.Status.STOP):
#         cmd = input()
#         if (cmd == 'f'):
#             print("started forward")
#             bot.drive_straight(constants.SPEED)
#             currentProgram.SLAMvals[0] = constants.SPEED
#             currentProgram.SLAMvals[1] = 0
#         elif (cmd == 'b'):
#             print("started back")
#             bot.drive_straight(-constants.SPEED)
#             currentProgram.SLAMvals[0] = -constants.SPEED
#             currentProgram.SLAMvals[1] = 0        
#         elif (cmd == 'r'):
#             print("started right")
#             bot.turn_clockwise(constants.TURN_SPEED)
#             currentProgram.SLAMvals[0] = 0
#             currentProgram.SLAMvals[1] = constants.TURN_SPEED_DEGREES    
#         elif (cmd == 'l'):
#             print("started left")
#             bot.turn_counter_clockwise(constants.TURN_SPEED)
#             currentProgram.SLAMvals[0] = 0
#             currentProgram.SLAMvals[1] = -constants.TURN_SPEED_DEGREES 
#         elif (cmd == 's'):
#             print("stopped")
#             bot.drive_straight(0)
#             currentProgram.SLAMvals[0] = 0
#             currentProgram.SLAMvals[1] = 0 
#         else:
#             print("bad command")


def run(currentProgram, bot):
    print("move thread")
    while (currentProgram.programStatus != constants.Status.STOP):
        if (currentProgram.programStatus != constants.Status.FOUND_OBSTACLE and
            currentProgram.programStatus != constants.Status.LIDAR_OBSTACLE):
            if(currentProgram.directionsQueue.qsize() > 0):
                if (currentProgram.programStatus != constants.Status.RUNNING):
                    # print("RUNNING")
                    currentProgram.programStatus = constants.Status.RUNNING

                cmd = currentProgram.directionsQueue.get()

                if(currentProgram.heading == cmd):
                    # straight
                    bot.drive_straight(constants.SPEED)
                    currentProgram.SLAMvals[0] = constants.SPEED
                    currentProgram.SLAMvals[1] = 0
                    time.sleep(constants.CHUNK_MOVE_TIME)

                elif(abs(currentProgram.heading - cmd) == 180):
                    # backwards
                    bot.turn_counter_clockwise(constants.TURN_SPEED)
                    currentProgram.SLAMvals[0] = 0
                    currentProgram.SLAMvals[1] = -constants.TURN_SPEED_DEGREES
                    time.sleep(constants.TURN_BACK)
                    bot.drive_straight(constants.SPEED)
                    currentProgram.SLAMvals[0] = constants.SPEED
                    currentProgram.SLAMvals[1] = 0
                    time.sleep(constants.CHUNK_MOVE_TIME)
                    currentProgram.heading = (currentProgram.heading + 180) % 360

                elif(currentProgram.heading - cmd == -90 or currentProgram.heading - cmd == 270):
                    # turn 90 left and drive
                    bot.turn_counter_clockwise(constants.TURN_SPEED)
                    currentProgram.SLAMvals[0] = 0
                    currentProgram.SLAMvals[1] = -constants.TURN_SPEED_DEGREES
                    time.sleep(constants.TURN_LEFT)
                    bot.drive_straight(constants.SPEED)
                    currentProgram.SLAMvals[0] = constants.SPEED
                    currentProgram.SLAMvals[1] = 0
                    time.sleep(constants.CHUNK_MOVE_TIME)
                    currentProgram.heading = (currentProgram.heading + 90) % 360

                elif(currentProgram.heading - cmd == 90 or currentProgram.heading - cmd == -270):
                    # turn 90 right and drive
                    bot.turn_clockwise(constants.TURN_SPEED)
                    currentProgram.SLAMvals[0] = 0
                    currentProgram.SLAMvals[1] = constants.TURN_SPEED_DEGREES
                    time.sleep(constants.TURN_RIGHT)
                    bot.drive_straight(constants.SPEED)
                    currentProgram.SLAMvals[0] = constants.SPEED
                    currentProgram.SLAMvals[1] = 0
                    time.sleep(constants.CHUNK_MOVE_TIME)
                    currentProgram.heading = (currentProgram.heading + 270) % 360
            else:
                if (currentProgram.programStatus != constants.Status.END_OF_PATH):
                    # print("END_OF_PATH")
                    currentProgram.programStatus = constants.Status.END_OF_PATH
                bot.drive_straight(0)
                currentProgram.SLAMvals[0] = 0
                currentProgram.SLAMvals[1] = 0


