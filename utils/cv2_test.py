#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#init the camera and grab a reference to the raw camera
camera = PiCamera()
rawCapture = PiRGBArray(camera)

#allow the camera to warmup
time.sleep(0.1)

#grab an image from the camera
camera.capture(rawCapture, format="bgr" )
image=rawCapture.array

cv2.imshow("Image", image)
cv2.waitKey(0)
