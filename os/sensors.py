import create2api
import json   # We'll use this to format the output



def monitor(currentProgram, bot):
	json.dumps(bot.sensor_state, indent=4)
	bot.get_packet(100)
	while (currentProgram.programStatus != constants.Status.STOP):
		print(json.dumps(bot.sensor_state, indent=4, sort_keys=False))
		currentProgram.foundObstacle = True

# bot = create2api.Create2()
# bot.start()
# bot.safe()
# json.dumps(bot.sensor_state, indent=4)
# bot.get_packet(100)
# while True:
# 	print(json.dumps(bot.sensor_state, indent=4, sort_keys=False))
# 	foundObstacle[0] = True