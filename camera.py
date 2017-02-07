from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime
import cv2

# Set up the camera
camera = PiCamera()
camera.framerate = 15
camera.resolution = (640, 480)
camera.hflip = True
camera.vflip = True
rawCapture=PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

shot_number = 0

# Get the image
for frame in camera.capture_continuous(rawCapture, format="bgr",
                                       use_video_port=True):

    image=frame.array

    cv2.imshow("Frame", image)
    key=cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break

    if key == ord("t"):
        camera.capture('/home/pi/capstone/pics/PIC%s.jpg' % \
                       str(datetime.datetime.now()))
        shot_number += 1

