#import os
import time
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar

Dataout = open("lidar_data.txt", "w")

SCAN_BYTE = b'\x20'
SCAN_TYPE = 129

PORT_NAME = "/dev/ttyUSB0"
lidar = RPLidar(None, PORT_NAME, baudrate=115200, timeout=3)

max_distance = 0

scan_data = [0] * 360

start_time = time.time()
try:
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            
            if(time.time() - start_time) > 4 :
                Dataout.close()
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                break
            
            scan_data[min([359, floor(angle)])] = distance
            Dataout.write(str(scan_data))
            Dataout.write("\n")
except KeyboardInterrupt:
    print('stopping')                
lidar.stop()
lidar.stop_motor()
lidar.disconnect()

