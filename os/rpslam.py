#!/usr/bin/env python3

'''
rpslam.py : BreezySLAM Python with SLAMTECH RP A1 Lidar
                 
Copyright (C) 2018 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''


from nav.constants import MAP_SIZE as MAP_SIZE_PIXELS
from nav.constants import MAP_SIZE_METERS as MAP_SIZE_METERS
import nav.constants as constants
import copy
from nav.pgm_utils import pgm_save
import time
from roboviz import MapVisualizer
from rplidar import RPLidar as Lidar
from breezyslam.sensors import RPLidarA1 as LaserModel
from breezyslam.algorithms import RMHC_SLAM

PORT1 = '/dev/ttyUSB1'
PORT0 = '/dev/ttyUSB0'

# Ideally we could use all 250 or so samples that the RPLidar delivers in one
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES = 50


def mm2pix(mm):
    return int(mm / (MAP_SIZE_METERS * 1000. / MAP_SIZE_PIXELS))


def slam(currentProgram):

    trajectory = []

    # Connect to Lidar unit
    try:
        lidar = Lidar(PORT1)
        currentProgram.roombaPort = PORT0
        iterator = lidar.iter_scans(1000)
        lidar.stop()
        next(iterator)
        print("ok")
    except:
        print("here")
        lidar.stop()
        lidar.disconnect()
        lidar = Lidar(PORT1)
        currentProgram.roombaPort = PORT0
        iterator = lidar.iter_scans(1000)
        lidar.stop()
        next(iterator)

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
    trajectory = []
    previous_distances = None
    previous_angles = None
    # start time
    start_time = time.time()
    prevTime = start_time

    while (currentProgram.programStatus != constants.Status.STOP):

        SLAMvel = currentProgram.SLAMvals[0]
        SLAMrot = currentProgram.SLAMvals[1]

        # Extract (quality, angle, distance) triples from current scan
        items = [item for item in next(iterator)]

        # Extract distances and angles from triples
        distances = [item[2] for item in items]
        angles = [item[1] for item in items]

        l =  list(zip(angles,distances))

        filtered = list(filter(lambda e: e[0]>=135 and e[0]<=225 and e[1]<300 , l))
        # s = sorted(l, key = lambda e: e[0])
        trigger_start = -100
        if (len(filtered) > constants.POINTS_THRESHOLD) and (time.time()-trigger_start >5):
            currentProgram.programStatus = constants.Status.LIDAR_OBSTACLE
            print("triggered")
            trigger_start = time.time()


        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(distances) > MIN_SAMPLES:
            # print("using speeds ", SLAMvel, SLAMrot)
            dt = time.time() - prevTime
            slam.update(distances, pose_change=(
                (SLAMvel*dt, SLAMrot*dt, dt)), scan_angles_degrees=angles)
            prevTime = time.time()
            previous_distances = copy.copy(distances)
            previous_angles = copy.copy(angles)
            # print("updated - if")

        # If not adequate, use previous
        elif previous_distances is not None:
            # print("using speeds ", SLAMvel, SLAMrot)
            dt = time.time() - prevTime
            slam.update(previous_distances, pose_change=(
                (SLAMvel*dt, SLAMrot*dt, dt)), scan_angles_degrees=previous_angles)
            prevTime = time.time()
            # print("updated - else")

        # Get current robot position
        x, y, theta = slam.getpos()
        [x_pix, y_pix] = [mm2pix(x), mm2pix(y)]
        currentProgram.robot_pos = [
            y_pix // constants.CHUNK_SIZE, x_pix // constants.CHUNK_SIZE]
        # print("robot_pos - ",x_pix // constants.CHUNK_SIZE,y_pix // constants.CHUNK_SIZE, theta)
        # Get current map bytes as grayscale
        slam.getmap(currentProgram.mapbytes)

    # Shut down the lidar connection
    pgm_save('ok.pgm', currentProgram.mapbytes,
             (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))

    lidar.stop()
    lidar.disconnect()
