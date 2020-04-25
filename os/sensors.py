import create2api
import json   # We'll use this to format the output
import nav.constants as constants
import queue
import time


def monitor(currentProgram, currmap, bot):
	# json.dumps(bot.sensor_state, indent=4)
	bot.get_packet(7)
	while (not currentProgram.stop):

		if (currentProgram.programStatus == constants.Status.LIDAR_OBSTACLE):

			currentProgram.directionsQueue = queue.Queue() # reset queue

			# drive back
			bot.drive_straight(-200)
			currentProgram.SLAMvals[0] = 0
			currentProgram.SLAMvals[1] = 0
			time.sleep(0.1)
			bot.drive_straight(0)	

			pos = currentProgram.robot_pos
			print("lidar obstacle")
			print(currentProgram.heading)
			if (currentProgram.obstacleLocation[0]):
				if (currentProgram.heading == constants.Heading.NORTH) : 
					if (pos[0]-1 > 0): 
						currmap.data_map[pos[0]-1][pos[1]-1] = constants.MapData.AVOID
				elif (currentProgram.heading == constants.Heading.SOUTH) : 
					if (pos[0]+1 < constants.NUM_CHUNKS): 
						currmap.data_map[pos[0]+1][pos[1]+1] = constants.MapData.AVOID        
				elif (currentProgram.heading == constants.Heading.EAST) : 
					if (pos[1]+1 < constants.NUM_CHUNKS): 
						currmap.data_map[pos[0]-1][pos[1]+1] = constants.MapData.AVOID 
				else: 
					if (pos[1]-1 > 0): 
						currmap.data_map[pos[0]+1][pos[1]-1] = constants.MapData.AVOID 

				currentProgram.obstacleLocation[0] = 0		


			if (currentProgram.obstacleLocation[1]):
				if (currentProgram.heading == constants.Heading.NORTH) : 
					if (pos[0]-1 > 0): 
						currmap.data_map[pos[0]-1][pos[1]] = constants.MapData.AVOID
				elif (currentProgram.heading == constants.Heading.SOUTH) : 
					if (pos[0]+1 < constants.NUM_CHUNKS): 
						currmap.data_map[pos[0]+1][pos[1]] = constants.MapData.AVOID        
				elif (currentProgram.heading == constants.Heading.EAST) : 
					if (pos[1]+1 < constants.NUM_CHUNKS): 
						currmap.data_map[pos[0]][pos[1]+1] = constants.MapData.AVOID 
				else: 
					if (pos[1]-1 > 0): 
						currmap.data_map[pos[0]][pos[1]-1] = constants.MapData.AVOID 		

				currentProgram.obstacleLocation[1] = 0		

			if (currentProgram.obstacleLocation[2]):
				if (currentProgram.heading == constants.Heading.NORTH) : 
					if (pos[0]-1 > 0): 
						currmap.data_map[pos[0]-1][pos[1]+1] = constants.MapData.AVOID
				elif (currentProgram.heading == constants.Heading.SOUTH) : 
					if (pos[0]+1 < constants.NUM_CHUNKS): 
						currmap.data_map[pos[0]+1][pos[1]-1] = constants.MapData.AVOID        
				elif (currentProgram.heading == constants.Heading.EAST) : 
					if (pos[1]+1 < constants.NUM_CHUNKS): 
						currmap.data_map[pos[0]+1][pos[1]+1] = constants.MapData.AVOID 
				else: 
					if (pos[1]-1 > 0): 
						currmap.data_map[pos[0]-1][pos[1]-1] = constants.MapData.AVOID 		

				currentProgram.obstacleLocation[2] = 0	

			print("stop???")

			# currentProgram.stop = True
			currentProgram.programStatus = constants.Status.END_OF_PATH



		if ((bot.sensor_state["wheel drop and bumps"]["bump right"] or 
			bot.sensor_state["wheel drop and bumps"]["bump left"]) and 
			(currentProgram.programStatus != constants.Status.FOUND_OBSTACLE)):
			print(bot.sensor_state["wheel drop and bumps"]["bump right"])
			print(bot.sensor_state["wheel drop and bumps"]["bump left"])
			print("obstacle!!!!!!!!!!!!!!!!!")
			currentProgram.programStatus = constants.Status.FOUND_OBSTACLE

			# drive back after hitting obstacle
			pos = currentProgram.robot_pos
			print(pos)
			if (currentProgram.heading == constants.Heading.NORTH) : 
				if (pos[0]-1 > 0): 
					currmap.data_map[pos[0]-1][pos[1]] = constants.MapData.AVOID
			elif (currentProgram.heading == constants.Heading.SOUTH) : 
				if (pos[0]+1 < constants.NUM_CHUNKS): 
					currmap.data_map[pos[0]+1][pos[1]] = constants.MapData.AVOID        
			elif (currentProgram.heading == constants.Heading.EAST) : 
				if (pos[1]+1 < constants.NUM_CHUNKS): 
					currmap.data_map[pos[0]][pos[1]+1] = constants.MapData.AVOID 
			else: 
				if (pos[1]-1 > 0): 
					currmap.data_map[pos[0]][pos[1]-1] = constants.MapData.AVOID 

			currentProgram.directionsQueue = queue.Queue() # reset queue
			# drive back
			bot.drive_straight(-200)
			currentProgram.SLAMvals[0] = 0
			currentProgram.SLAMvals[1] = 0
			time.sleep(0.1)
			bot.drive_straight(0)
			# reset status

			currentProgram.programStatus = constants.Status.END_OF_PATH
			bot.get_packet(7)

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