import time
import ultrasonic
import RPi.GPIO as GPIO


# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.

ultrasonic_sensor = ultrasonic.SRF05_Ultrasonic_Sensor(trigger=19, echo=26)
motors = movement.Motors(motor1_in1_pin=27, motor1_in2_pin=22, motorpwm1_in1_pin = 4, 
  	motor2_in1_pin = 24, motor2_in2_pin = 25, motorpwm2_in1_pin = 18, power_range = 100)


try:
	motors.start(60)
  	
  	while (ultrasonic_sensor.get_distance() > 15):
  		pass

  	motors.stop()

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()


