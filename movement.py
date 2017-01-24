import RPi.GPIO as io
import time

io.setmode(io.BCM)

# Define the global speed
global_speed = 0

# Setup motor 1
motor1_in1_pin = 27
motor1_in2_pin = 22

io.setup(motor1_in1_pin, io.OUT)
io.setup(motor1_in2_pin, io.OUT)

# setup pulse-width modulation for motor 1
motorpwm1_in1_pin = 4
io.setup(motorpwm1_in1_pin, io.OUT)
motorpwm1 = io.PWM(4,100)

# Initial output for motor 1
io.output(motor1_in1_pin, True)
io.output(motor1_in2_pin, False)
motorpwm1.start(0)

# Setup motor 2 
motor2_in1_pin = 24
motor2_in2_pin = 25

io.setup(motor2_in1_pin, io.OUT)
io.setup(motor2_in2_pin, io.OUT)

motorpwm2_in1_pin = 18
io.setup(motorpwm2_in1_pin, io.OUT)
motorpwm2 = io.PWM(motorpwm2_in1_pin ,100)

io.output(motor2_in1_pin, True)
io.output(motor2_in2_pin, False)
motorpwm2.start(global_speed)

def forward():
	print("Going forwards")
	io.output(motor2_in1_pin, True)
	io.output(motor2_in2_pin, False)	
	io.output(motor1_in1_pin, True)
	io.output(motor1_in2_pin, False)

def backward(): 
	print("Going backwards") 
        io.output(motor2_in1_pin, False)
        io.output(motor2_in2_pin, True)
        io.output(motor1_in1_pin, False)
        io.output(motor1_in2_pin, True)

def start(speed):
	print("Starting the motors at speed %s" % speed)
	global global_speed
	global_speed = speed
	motorpwm1.ChangeDutyCycle(global_speed)
        motorpwm2.ChangeDutyCycle(global_speed)

def accelerate(step):
	global global_speed
	if (global_speed + step <= 100):
                global_speed = global_speed + step
		print("Accelerating by %s. New speed is %s" % \
			(step, global_speed))
        	motorpwm1.ChangeDutyCycle(global_speed)
       	 	motorpwm2.ChangeDutyCycle(global_speed)
	else:
		print("Already reached max speed")

def brake(step): 
	global global_speed
        if (global_speed  - step >= 0):
                global_speed = global_speed - step
        	motorpwm1.ChangeDutyCycle(global_speed)
        	motorpwm2.ChangeDutyCycle(global_speed)
        else:
                print("Already going too slowly")

def stop(): 
        global global_speed
	global_speed = 0
        motorpwm1.ChangeDutyCycle(global_speed)
        motorpwm2.ChangeDutyCycle(global_speed)
        print("Stopping")
try:
#    while 1:
#               motorpwm1.ChangeDutyCycle(60)
        #        motorpwm1.ChangeDutyCycle(60)
        # for dc in range(0, 30, 5):
	backward()
	start(50)
	time.sleep(1)
	accelerate(20)
	time.sleep(1)
	stop()
	backward()
	start(50)
	#brake(20)
	time.sleep(3)
except KeyboardInterrupt:
    pass
#except: 
#	print("Unspecified error") 
#	pass


motorpwm1.stop()
motorpwm2.stop()
io.cleanup()

