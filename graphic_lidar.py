#import os
import pygame
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar


W = 640
H = 480

SCAN_BYTE = b'\x20'
SCAN_TYPE = 129


# Setup pygame
pygame.display.init()
lcd = pygame.display.set_mode((H,H))
pygame.mouse.set_visible(False)
lcd.fill((200,0,0))
pygame.display.update()


# Setup the RPLidar
PORT_NAME = "/dev/ttyUSB0"
lidar = RPLidar(None, PORT_NAME, timeout=3)

# used to scale data to fit on the screen
max_distance = 0


def process_data(data):
    global max_distance
    lcd.fill((0,0,0))
    point = ( int(W / 2) , int(H / 2) )
    
    pygame.draw.circle(lcd,pygame.Color(255, 255, 255),point,10 )
    pygame.draw.circle(lcd,pygame.Color(100, 100, 100),point,100 , 1 )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( 0, int(H/2)),( W , int(H/2) ) )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( int(W/2),0),( int(W/2) , H ) )

    for angle in range(360):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = ( int(W / 2) + int(x / max_distance * (W/2)), int(H/2) + int(y / max_distance * (H/2) ))
            pygame.draw.circle(lcd,pygame.Color(255, 0, 0),point,2 )
    pygame.display.update()

scan_data = [0] * 360

try:
    #    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print("Stopping.")
lidar.stop()
lidar.disconnect()
