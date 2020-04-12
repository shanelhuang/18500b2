import create2api
import threading

def run(directionsQueue):
	print('thread')
	print(directionsQueue)
	while True:
		if(directionsQueue.qsize() > 0):
			print(directionsQueue.get())


		# cmd = input()
		# if (cmd == 'f'):
		# 	# bot.drive_straight(20)
		# 	print('forward')
		# elif (cmd == 'b'):
		# 	# bot.drive_straight(-20)
		# 	print('backward')
		# elif (cmd == 'r'):
		# 	# bot.turn_clockwise(200)
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