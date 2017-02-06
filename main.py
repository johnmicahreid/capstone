import time
import ultrasonic
import movement
import led_control
import RPi.GPIO as GPIO

GPIO.cleanup()
# GPIO pin numbers

# ultrasonic
trigger_pin = 19
echo_pin = 26

# motors 
motor1_in1_pin=27
motor1_in2_pin=22
motorpwm1_in1_pin = 4
motor2_in1_pin = 24
motor2_in2_pin = 25
motorpwm2_in1_pin = 18

# LED
led_pin = 21

# Create the objects we will be using
ultrasonic_sensor = ultrasonic.SRF05_Ultrasonic_Sensor(trigger=trigger_pin, echo=echo_pin)
motors = movement.Motors(motor1_in1_pin=27, motor1_in2_pin=22, motorpwm1_in1_pin = 4, 
  	motor2_in1_pin = 24, motor2_in2_pin = 25, motorpwm2_in1_pin = 18, power_range = 100)
led = led_control.LED(led_pin = led_pin, brightness = 0)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:
        led.set_brightness(100)
        motors.start(60)

        while (ultrasonic_sensor.get_distance() > 15):
                pass

        motors.stop()
        led.stop()

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()


