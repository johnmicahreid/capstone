# The purpose of this script is to detect a leading car 
# (as represented by a green ball). This information will be used
# to control the drive script for the follower cars. 

# This code is based on a PyImageSearch tutorial 
# http://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
import cv2
import time

class CarDetector(object):

	def __init__(self):
		self.img = None
		self.xpos = 0
		self.ypos = 0
		self.hsvLower = (29, 86, 6) ## Green in HSV space
		self.hsvUpper = (64, 255, 255)
		self.centre = None
		self.radius = None

	def get_centre(self, img):
		self.img = img
		blurred = cv2.GaussianBlur(self.img, (11, 11), 0)
		hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
	 
		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, self.hsvLower, self.hsvUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
	 
		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			self.centre = (x, y)
			self.radius = radius
	 
			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame
				cv2.circle(self.img, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)

	def show_img(self):
		cv2.imshow("Frame", self.img)
		
	def get_offset(self):
		# Centre of the frame minus centre of the x-coordinate
		return self.img.shape[0]/2 - self.centre[0] 

from picamera.array import PiRGBArray
from picamera import PiCamera

# Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 16
rawCapture=PiRGBArray(camera, size=(640, 480))
camera.hflip = True
camera.vflip = True
time.sleep(0.1)

# Car detector
card = CarDetector()

for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port=True):


    image=frame.array
    card.get_centre(image)
    card.show_img()
    rawCapture.truncate(0)

    key=cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        print("User shutdown")
        break

