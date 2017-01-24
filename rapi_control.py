#-*- coding: utf-8 -*-
# Version: 0.1
# Author: John Reid
# Date: November 2016

import RPi.GPIO as io

io.setmode(io.BCM)


import sys, tty, termios, time
import os

# set variables Motor speed.

motorLspeed = 0
motorRspeed = 0

maxspeed = 40

minspeed = 0

acceleration = 0

speedstep = 5

# set variable actual direction

direction =""

# set variable for turning on spot

spot = "false"

# Here we configure the PWM settings for
# the four DC motors. It defines the two GPIO
# pins used for the input on the L298 H-Bridge,
# starts the PWM and sets the
# motors’ speed initial to 0

led_pin = 21
io.setup(led_pin, io.OUT)
led = io.PWM(led_pin, 50)
led.start(30)

motor1_in1_pin = 27
motor1_in2_pin = 22
io.setup(motor1_in1_pin, io.OUT)
io.setup(motor1_in2_pin, io.OUT)

motor2_in1_pin = 24
motor2_in2_pin = 25
io.setup(motor2_in1_pin, io.OUT)
io.setup(motor2_in2_pin, io.OUT)

# set PWM for motor1 to 0

motorpwm1_in1_pin = 4
#motorpwm1_in2_pin = 17

io.setup(motorpwm1_in1_pin, io.OUT)
#io.setup(motorpwm1_in2_pin, io.OUT)

motorpwm1 = io.PWM(4,100)
#motorpwm1 = io.PWM(17,100)

motorpwm1.start(0)
motorpwm1.ChangeDutyCycle(0)

# set PWM for motor2 to 0

motorpwm2_in1_pin = 18
#motorpwm2_in2_pin = 23

io.setup(motorpwm2_in1_pin, io.OUT)
#io.setup(motorpwm2_in2_pin, io.OUT)

motorpwm2 = io.PWM(18,100)
#motorpwm2 = io.PWM(23,100)

motorpwm2.start(0)
motorpwm2.ChangeDutyCycle(0)

# The catch method can determine which key has been pressed
# by the user on the keyboard.

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

# Here we define the methods used to determine
# whether a motor needs to spin forward or backwards.
# If both pins match, the motor will not turn.

def reverse():
	io.output(motor1_in1_pin, True)
	io.output(motor1_in2_pin, False)
	io.output(motor2_in1_pin, False)
	io.output(motor2_in2_pin, True)

def forward():
	io.output(motor1_in1_pin, False)
	io.output(motor1_in2_pin, True)
	io.output(motor2_in1_pin, True)
	io.output(motor2_in2_pin, False)

# stop the motors

def stop():
	io.output(motor1_in1_pin, False)
	io.output(motor1_in2_pin, False)
	io.output(motor2_in1_pin, False)
	io.output(motor2_in2_pin, False)
	motorLspeed = 0
	motorRspeed = 0
	acceleration = 0

# This functions sets the motor speed.

def setmotorspeed(motorLspeed, motorRspeed, acceleration):
	if(acceleration > 0):
		forward()

	if(acceleration > maxspeed):
		acceleration = maxspeed
		motorLspeed = acceleration
		motorRspeed = acceleration
	
	elif(acceleration == 0):
		motorLspeed = acceleration
		motorRspeed = acceleration
		stop()

	elif(acceleration < (maxspeed *-1)):
		acceleration = (maxspeed * -1)
	else:
		reverse()
		motorLspeed = (acceleration * -1)
		motorRspeed = (acceleration * -1)
		motorLspeed, motorRspeed = check_motorpseed(motorLspeed, motorRspeed)

	return motorLspeed, motorRspeed, acceleration

# This function is used for left steering

def left(motorLspeed, motorRspeed):
	if(motorRspeed < motorLspeed):
		motorRspeed = motorRspeed + speedstep
	else:
		motorLspeed = motorLspeed - speedstep
		motorLspeed, motorRspeed = check_motorpseed(motorLspeed, motorRspeed)
	return motorLspeed, motorRspeed

#This function is used for right steering

def right(motorLspeed, motorRspeed):
	if(motorLspeed < motorRspeed):
		motorLspeed = motorLspeed + speedstep
	else:
		motorRspeed = motorRspeed-speedstep
		motorLspeed, motorRspeed = check_motorpseed(motorLspeed, motorRspeed)
	return motorLspeed, motorRspeed

# check the motorspeed if it is correct and in max/min range

def check_motorpseed(motorLspeed, motorRspeed):
	if (motorLspeed < minspeed):
		 motorLspeed = minspeed
 	if (motorLspeed > maxspeed):
		motorLspeed = maxspeed
	if (motorRspeed < minspeed):
		 motorRspeed = minspeed
	if (motorRspeed > maxspeed):
		motorRspeed = maxspeed

	return motorLspeed, motorRspeed

# Setting the PWM pins to false so the motors will not move
# until the user presses the first key

io.output(motor1_in1_pin, False)
io.output(motor1_in2_pin, False)
io.output(motor2_in1_pin, False)
io.output(motor2_in2_pin, False)

# Instructions for when the user has an interface

print("w/s: direction")
print("a/d: steering")
print("q: stops the motors")
print("x: exit")

# Infinite loop
# The loop will not end until the user presses the
# exit key "X" or the program crashes.�

while True:

# Keyboard character retrieval method. This method will save
# the pressed key into the variable char

	char = getch()

	print motorLspeed, motorRspeed, acceleration

	# The car will drive forward when the “w” key is pressed

	if(char == "w"):
		acceleration = acceleration + speedstep
		motorLspeed, motorRspeed, acceleration = setmotorspeed(motorLspeed, motorRspeed, acceleration)
		motorpwm1.ChangeDutyCycle(motorLspeed)
		motorpwm2.ChangeDutyCycle(motorRspeed)

	# The car will reverse when the “s” key is pressed

	if(char =="s"):
		acceleration = acceleration-speedstep
		motorLspeed, motorRspeed, acceleration = setmotorspeed(motorLspeed, motorRspeed, acceleration)
		motorpwm1.ChangeDutyCycle(motorLspeed)
		motorpwm2.ChangeDutyCycle(motorRspeed)

	# Stop the motors

	if(char =="q"):
		motorLspeed = 0
		motorRspeed = 0
		stop()

	# The “d” key will toggle the steering right

	if(char =="d"):
		motorLspeed, motorRspeed = right(motorLspeed, motorRspeed)
		motorpwm1.ChangeDutyCycle(motorLspeed)
		motorpwm2.ChangeDutyCycle(motorRspeed)

	# The “a” key will toggle the steering left

	if(char =="a"):
		motorLspeed, motorRspeed = left(motorLspeed, motorRspeed)
		motorpwm1.ChangeDutyCycle(motorLspeed)
		motorpwm2.ChangeDutyCycle(motorRspeed)

	# The “x” key will break the loop and exit the program

	if(char =="x"):
		print("Program Ended")
		break

# The keyboard character variable char has to be set blank. We need

# to set it blank to save the next key pressed by the user

char = ""

# Program will clean up all GPIO settings and terminates

io.cleanup()

# End

