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


import time
import RPi.GPIO as GPIO

class SRF05_Ultrasonic_Sensor(object):

  def __init__(self, trigger, echo):
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


  def get_distance(self):
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


