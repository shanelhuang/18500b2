
import create2api

bot = create2api.Create2()
bot.start()
bot.safe()

while True:
	cmd = raw_input()
	if (cmd == 'f'):
		bot.drive_straight(20)
	elif (cmd == 'b'):
		bot.drive_straight(-20)
	elif (cmd == 'r'):
		bot.turn_clockwise(200)
	elif (cmd == 'l'):
		bot.turn_counter_clockwise(200)
	elif (cmd == 's'):
		bot.drive_straight(0)
	else:
		print("bad command")