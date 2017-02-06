import RPi.GPIO as GPIO
import time


class Motors(object):

  def __init__(self, motor1_in1_pin=27, motor1_in2_pin=22, motorpwm1_in1_pin = 4, 
      motor2_in1_pin = 24, motor2_in2_pin = 25, motorpwm2_in1_pin = 18, power_range = 100):

      GPIO.setmode(GPIO.BCM)

      # Define the global speed
      self.speed = 0

      # Setup motor 1
      self.motor1_in1_pin = motor1_in1_pin
      self.motor1_in2_pin = motor1_in2_pin

      GPIO.setup(self.motor1_in1_pin, GPIO.OUT)
      GPIO.setup(self.motor1_in2_pin, GPIO.OUT)

      # setup pulse-width modulation for motor 1
      self.motorpwm1_in1_pin = motorpwm1_in1_pin
      GPIO.setup(self.motorpwm1_in1_pin, GPIO.OUT)
      self.motorpwm1 = GPIO.PWM(self.motorpwm1_in1_pin, power_range)

      # Initial output for motor 1
      GPIO.output(self.motor1_in1_pin, True)
      GPIO.output(self.motor1_in2_pin, False)
      self.motorpwm1.start(0)

      # Setup motor 2 
      self.motor2_in1_pin = motor2_in1_pin
      self.motor2_in2_pin = motor2_in2_pin

      GPIO.setup(self.motor2_in1_pin, GPIO.OUT)
      GPIO.setup(self.motor2_in2_pin, GPIO.OUT)

      self.motorpwm2_in1_pin = motorpwm2_in1_pin
      GPIO.setup(self.motorpwm2_in1_pin, GPIO.OUT)
      self.motorpwm2 = GPIO.PWM(self.motorpwm2_in1_pin, power_range)

      GPIO.output(self.motor2_in1_pin, True)
      GPIO.output(self.motor2_in2_pin, False)

      self.motorpwm2.start(self.speed)

  def forward(self):
      print("Going forwards")
      GPIO.output(self.motor2_in1_pin, True)
      GPIO.output(self.motor2_in2_pin, False)	
      GPIO.output(self.motor1_in1_pin, True)
      GPIO.output(self.motor1_in2_pin, False)

  def backward(self): 
      print("Going backwards") 
      GPIO.output(self.motor2_in1_pin, False)
      GPIO.output(self.motor2_in2_pin, True)
      GPIO.output(self.motor1_in1_pin, False)
      GPIO.output(self.motor1_in2_pin, True)

  def start(self, speed):
      print("Starting the motors at speed %s" % speed)
      self.speed = speed
      self.motorpwm1.ChangeDutyCycle(self.speed)
      self.motorpwm2.ChangeDutyCycle(self.speed)

  def accelerate(self, step):
      if (self.speed + step <= 100):
        self.speed = speed + step
        print("Accelerating by %s. New speed is %s" % (step, self.speed))
        self.motorpwm1.ChangeDutyCycle(self.speed)
        self.motorpwm2.ChangeDutyCycle(self.speed)
      else:
        print("Already reached max speed")

  def brake(self, step): 
    if (self.speed  - step >= 0):
        self.speed = self.speed - step
        self.motorpwm1.ChangeDutyCycle(self.speed)
        self.motorpwm2.ChangeDutyCycle(self.speed)
    else:
        print("Already going too slowly")

  def stop(self): 
      self.speed = 0
      self.motorpwm1.ChangeDutyCycle(self.speed)
      self.motorpwm2.ChangeDutyCycle(self.speed)
      print("Stopping")
