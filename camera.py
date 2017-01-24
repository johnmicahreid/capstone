from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (800, 400)
camera.framerate = 15

camera.start_preview(alpha=200)
sleep(10)
camera.capture('/home/pi/Desktop/test.jpg') 
camera.stop_preview()
