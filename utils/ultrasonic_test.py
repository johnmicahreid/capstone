#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic.py
# Measure distance using an ultrasonic module
#
# Author : Matt Hawkins
# Date   : 09/01/2013
# Modified: John Reid
# Date    : 2017/01/30
# Import required Python libraries


import time, cv2
import RPi.GPIO as GPIO
import numpy as np

class SRF05_Ultrasonic_Sensor(object):

  def __init__(self, trigger, echo, processNoise = 0.00003, measurementNoise = 0.03):
    # Set up the Kalman filter
    self.meas=[]
    self.pred=[]
    self.mp = np.array((1,1),np.float32) # measurement
    self.tp = np.zeros((1,1),np.float32) # tracked / prediction

    self.kalman = cv2.KalmanFilter(2,1) # 2D state (distance and velocity), 1D measurement (distance)
    self.kalman.measurementMatrix = np.array([[1,1]], np.float32)
    self.kalman.transitionMatrix = np.array([[1,1], [0,1]], np.float32)
    self.kalman.processNoiseCov = np.array([[1,0], [0,1]], np.float32) * processNoise
    self.kalman.measurementNoiseCov = np.array([[1]], np.float32) * measurementNoise

	# Set up the GPIO pins
    self.trigger = trigger
    self.echo = echo
    GPIO.setmode(GPIO.BCM)
    # Set pins as output and input
    GPIO.setup(self.trigger, GPIO.OUT)  # Trigger
    GPIO.setup(self.echo, GPIO.IN)      # Echo

    # Set trigger to False (Low)
    GPIO.output(self.trigger, False)

  
  def get_distance_raw(self):
    # This function measures a distance
    GPIO.output(self.trigger, True)
    time.sleep(0.00001)
    GPIO.output(self.trigger, False)
    start = time.time()

    while GPIO.input(self.echo)==0:
      pass

    while GPIO.input(self.echo)==1:
      pass

    stop = time.time()
    elapsed = stop-start
    distance = (elapsed * 34300) / 2 # Divide by 2 to account for the echo

    return distance

  def get_distance_filtered(self):
  	mp = np.array([[self.get_distance_raw()]], np.float32)
  	self.meas.append(mp[0][0])
  	self.kalman.correct(mp)
  	tp=self.kalman.predict()
  	self.pred.append(tp[0][0])
  	return tp[0][0]

  def get_distance_avg_of_3(self):
    # This function takes 3 measurements and
    # returns the average.
    distance1=self.get_distance_raw()
    time.sleep(0.1)
    distance2=self.get_distance_raw()
    time.sleep(0.1)
    distance3=self.get_distance_raw()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    print("%s cm" % distance)
    return distance

  def stop(self):
    GPIO.cleanup()


ultra = SRF05_Ultrasonic_Sensor(19, 26)
while(True):
	dist = ultra.get_distance_raw() 
	print(dist)
	time.sleep(0.1)
