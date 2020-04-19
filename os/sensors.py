import create2api
import json   # We'll use this to format the output
import nav.constants as constants



def monitor(currentProgram, bot):
	# json.dumps(bot.sensor_state, indent=4)
	bot.get_packet(7)
	while (currentProgram.programStatus != constants.Status.STOP):
		if (bot.sensor_state["wheel drop and bumps"]["bump right"] or 
			bot.sensor_state["wheel drop and bumps"]["bump left"]):
			currentProgram.programStatus = constants.Status.FOUND_OBSTACLE
		bot.get_packet(7)

# bot = create2api.Create2('/dev/ttyUSB1')
# bot.start()
# bot.safe()
# bot.full()

# json.dumps(bot.sensor_state, indent=4)
# bot.get_packet(7)
# while True:
# 	print(bot.sensor_state["wheel drop and bumps"]["bump right"],bot.sensor_state["wheel drop and bumps"]["bump left"])
# 	bot.get_packet(7)
# 	# foundObstacle[0] = True