import RPi.GPIO as GPIO
import time


class Motors(object):

  def __init__(self, maxspeed = 80, motor_left_in1_pin=27, motor_left_in2_pin=22, motorpwm_left_in1_pin = 4, 
      motor_right_in1_pin = 24, motor_right_in2_pin = 25, motorpwm_right_in1_pin = 18, power_range = 100):

      GPIO.setmode(GPIO.BCM)

      # Define the global speed
      self.leftspeed = 0
      self.rightspeed = 0
      self.maxspeed = maxspeed

      # Setup left motor 
      self.motor_left_in1_pin = motor_left_in1_pin
      self.motor_left_in2_pin = motor_left_in2_pin

      GPIO.setup(self.motor_left_in1_pin, GPIO.OUT)
      GPIO.setup(self.motor_left_in2_pin, GPIO.OUT)

      # setup pulse-width modulation for left motor
      self.motorpwm_left_in1_pin = motorpwm_left_in1_pin
      GPIO.setup(self.motorpwm_left_in1_pin, GPIO.OUT)
      self.motorpwm_left = GPIO.PWM(self.motorpwm_left_in1_pin, power_range)

      # Initial output for motor 1
      GPIO.output(self.motor_left_in1_pin, True)
      GPIO.output(self.motor_left_in2_pin, False)
      self.motorpwm_left.start(self.leftspeed)

      # Setup motor 2 
      self.motor_right_in1_pin = motor_right_in1_pin
      self.motor_right_in2_pin = motor_right_in2_pin

      GPIO.setup(self.motor_right_in1_pin, GPIO.OUT)
      GPIO.setup(self.motor_right_in2_pin, GPIO.OUT)

      self.motorpwm_right_in1_pin = motorpwm_right_in1_pin
      GPIO.setup(self.motorpwm_right_in1_pin, GPIO.OUT)
      self.motorpwm_right = GPIO.PWM(self.motorpwm_right_in1_pin, power_range)

      GPIO.output(self.motor_right_in1_pin, True)
      GPIO.output(self.motor_right_in2_pin, False)

      self.motorpwm_right.start(self.rightspeed)

  def get_speeds(self):
      return(self.leftspeed, self.rightspeed)

  def forward(self):
      print("Going forwards")
      GPIO.output(self.motor_right_in1_pin, True)
      GPIO.output(self.motor_right_in2_pin, False)	
      GPIO.output(self.motor_left_in1_pin, True)
      GPIO.output(self.motor_left_in2_pin, False)

  def backward(self): 
      print("Going backwards") 
      GPIO.output(self.motor_right_in1_pin, False)
      GPIO.output(self.motor_right_in2_pin, True)
      GPIO.output(self.motor_left_in1_pin, False)
      GPIO.output(self.motor_left_in2_pin, True)

  def start(self, speed):
      print("Starting the motors at speed %s" % speed)
      self.leftspeed = speed
      self.rightspeed = speed
      self.motorpwm_left.ChangeDutyCycle(self.leftspeed)
      self.motorpwm_right.ChangeDutyCycle(self.rightspeed)

  def turn(self, angle):
      print("Turning the car %d amount" % angle)
      self.leftspeed = self.leftspeed + angle
      self.rightspeed = self.rightspeed - angle
      self.motorpwm_left.ChangeDutyCycle(self.leftspeed)
      self.motorpwm_right.ChangeDutyCycle(self.rightspeed)

  def set_LR_speed(self, offset, steering_angle):
      if offset < -320:
        offset = -320
      if offset > 320:
        offset = 320
      offset = offset * steering_angle
      if offset > 0:
        self.leftspeed = int(self.maxspeed * (1 - offset))
        self.rightspeed = self.maxspeed
      else:
        self.leftspeed = self.maxspeed
        self.rightspeed = int(self.maxspeed * (1 + offset))
        self.motorpwm_left.ChangeDutyCycle(self.leftspeed)
        self.motorpwm_right.ChangeDutyCycle(self.rightspeed)   

  def accelerate(self, step):
      if (self.leftspeed + step <= 100 and self.rightspeed + step <= 100):
        self.leftspeed = self.leftspeed + step
        self.rightspeed = self.rightspeed + step
        print("Accelerating by %s. New speeds are %s %s" % (step, self.leftspeed, self.rightspeed))
        self.motorpwm_left.ChangeDutyCycle(self.leftspeed)
        self.motorpwm_right.ChangeDutyCycle(self.rightspeed)
      else:
        print("Already reached max speed")

  def brake(self, step): 
    if (self.leftspeed  - step >= 0 and self.rightspeed - step >= 0):
        self.leftspeed = self.leftspeed - step
        self.rightspeed = self.rightspeed - step
        self.motorpwm_left.ChangeDutyCycle(self.leftspeed)
        self.motorpwm_right.ChangeDutyCycle(self.rightspeed)
    else:
        print("Already going too slowly")

  def straighten(self):
    newspeed = max(self.leftspeed, self.rightspeed)
    self.leftspeed = newspeed
    self.rightspeed = newspeed
    self.motorpwm_left.ChangeDutyCycle(self.leftspeed)
    self.motorpwm_right.ChangeDutyCycle(self.rightspeed)
    print("Straightening out")

  def stop(self): 
      self.leftspeed = 0
      self.rightspeed = 0
      self.motorpwm_left.ChangeDutyCycle(self.leftspeed)
      self.motorpwm_right.ChangeDutyCycle(self.rightspeed)
      print("Stopping")
