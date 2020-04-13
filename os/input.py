import create2api
import threading
import nav.constants as constants


def run(directionsQueue):
	heading = constants.Heading.NORTH
	print('thread')
	print('\n')
	print(directionsQueue)
	while True:
		if(directionsQueue.qsize() > 0):
			cmd = directionsQueue.get()
			print(cmd)
			if(heading == cmd):
				print('straight')
				# drive straight
				bot.drive_straight(20)
			elif(abs(heading - cmd) == 180):
				print('backward')
				# turn 180 and drive
				bot.turn_counter_clockwise(1000)
				bot.drive_straight(20)
				heading = (heading + 180) % 360
			elif(heading - cmd == -90 or heading - cmd == 270):
				print('left')
				# turn 90 left and drive
				bot.turn_counter_clockwise(200)
				bot.drive_straight(20)
				heading = (heading + 90) % 360
			elif(heading - cmd == 90 or heading - cmd == -270):
				print('right')
				# turn 90 right and drive
				bot.turn_clockwise(200)
				bot.drive_straight(20)
				heading = (heading + 270) % 360




			# if (cmd == constants.Heading.NORTH):
			# 	bot.drive_straight(20)
			# elif (cmd == 'b'):
			# 	# bot.drive_straight(-20)
			# 	print('backward')
			# elif (cmd == constants.Heading.EAST):
			# 	bot.turn_clockwise(200)
			# 	sleep()
			# 	print('right')
			# elif (cmd == 'l'):
			# 	# bot.turn_counter_clockwise(200)
			# 	print('left')
			# elif (cmd == 's'):
			# 	# bot.drive_straight(0)
			# 	print('stop')
			# elif(cmd == 'exit'):
			# 	return
			# else:
			# 	print("bad command")