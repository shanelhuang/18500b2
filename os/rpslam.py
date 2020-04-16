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
import copy
from nav.pgm_utils import pgm_save
import time
from roboviz import MapVisualizer
import matplotlib
from rplidar import RPLidar as Lidar
from breezyslam.sensors import RPLidarA1 as LaserModel
from breezyslam.algorithms import RMHC_SLAM
LIDAR_DEVICE = '/dev/ttyUSB0'


# Ideally we could use all 250 or so samples that the RPLidar delivers in one
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES = 200


# matplotlib.use('tkagg')


def slam(currentProgram):

    trajectory = []

    # Connect to Lidar unit
    lidar = Lidar(LIDAR_DEVICE)

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Set up a SLAM display
    viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')

    # Initialize an empty trajectory
    trajectory = []

    # Initialize empty map - done in main.py
    # mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    # Create an iterator to collect scan data from the RPLidar
    iterator = lidar.iter_scans()

    # We will use these to store previous scan in case current scan is inadequate
    previous_distances = None
    previous_angles = None

    # First scan is crap, so ignore it
    next(iterator)

    # start time
    start_time = time.time()

    prevTime = start_time
    print("start")

    while True:

        SLAMvel = currentProgram.SLAMvals[0]
        SLAMrot = currentProgram.SLAMvals[1]

        # Extract (quality, angle, distance) triples from current scan
        items = [item for item in next(iterator)]

        # Extract distances and angles from triples
        distances = [item[2] for item in items]
        angles = [item[1] for item in items]

        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(distances) > MIN_SAMPLES:
            slam.update(distances, pose_change=(
                (SLAMvel, SLAMrot, time.time() - prevTime)), scan_angles_degrees=angles)
            prevTime = time.time()
            previous_distances = copy.copy(distances)
            previous_angles = copy.copy(angles)
            print("updated - if")

        # If not adequate, use previous
        elif previous_distances is not None:
            slam.update(previous_distances, pose_change=(
                (SLAMvel, SLAMrot, time.time() - prevTime)), scan_angles_degrees=previous_angles)
            prevTime = time.time()
            print("updated - else")

        # Get current robot position
        x, y, theta = slam.getpos()

        # Get current map bytes as grayscale
        slam.getmap(currentProgram.mapbytes)

        if(time.time() - start_time > 5):
            pgm_save('ok.pgm', currentProgram.mapbytes,
                     (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))
            exit(0)

        # Display map and robot pose, exiting gracefully if user closes it
        # if not viz.display(x/1000., y/1000., theta, mapbytes):
        #     exit(0)

    # Shut down the lidar connection
    lidar.stop()
    lidar.disconnect()
