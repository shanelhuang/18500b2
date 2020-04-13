import create2api
import threading
import nav.constants as constants

heading = constants.Heading.NORTH

def run(directionsQueue):
	print('thread')
	print(directionsQueue)
	while True:
		if(directionsQueue.qsize() > 0):
			cmd = directionsQueue.get()
			print(cmd)
			if (cmd == constants.Heading.NORTH):
				bot.drive_straight(20)
			elif (cmd == 'b'):
				# bot.drive_straight(-20)
				print('backward')
			elif (cmd == constants.Heading.EAST):
				bot.turn_clockwise(200)
				sleep()
				print('right')
			elif (cmd == 'l'):
				# bot.turn_counter_clockwise(200)
				print('left')
			elif (cmd == 's'):
				# bot.drive_straight(0)
				print('stop')
			elif(cmd == 'exit'):
				return
			else:
				print("bad command")