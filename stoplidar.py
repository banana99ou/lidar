from adafruit_rplidar import RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
lidar.stop()
lidar.stop_motor()
lidar.disconnect()
print("ran")