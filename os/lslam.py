
import create2api
import time


bot = create2api.Create2('/dev/ttyUSB0')
bot.start()
bot.safe()

while True:
	cmd = input()
	if (cmd == 'f'):
		bot.drive_straight(20)
	elif (cmd == 'b'):
		bot.drive_straight(-20)
	elif (cmd == 'r'):
		bot.turn_clockwise(20)
	elif (cmd == 'l'):
		bot.turn_counter_clockwise(300)
		time.sleep(10)
		bot.drive_straight(0)
		bot.drive_straight(0)
	elif (cmd == 's'):
		bot.drive_straight(0)
	else:
		print("bad command")