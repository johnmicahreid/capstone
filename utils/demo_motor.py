import RPi.GPIO as io
import time

io.setmode(io.BCM)

# Setup motor 1
motor1_in1_pin = 27
motor1_in2_pin = 22

io.setup(motor1_in1_pin, io.OUT)
io.setup(motor1_in2_pin, io.OUT)

#setup pulse-width modulation for motor 1
motorpwm1_in1_pin = 4
io.setup(motorpwm1_in1_pin, io.OUT)
motorpwm1 = io.PWM(4,100)

#Initial output for motor 1
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
motorpwm2.start(0)

try:
#    while 1:
#        for dc in range(0, 30, 5):
        print("Starting motors")
        motorpwm1.ChangeDutyCycle(60)
        motorpwm2.ChangeDutyCycle(60)
        time.sleep(10)
except KeyboardInterrupt:
        pass

motorpwm1.stop()
motorpwm2.stop()
io.cleanup()
