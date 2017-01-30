import time
import ultrasonic
import RPi.GPIO as GPIO


# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.

ultrasonic_sensor = ultrasonic.SRF05_Ultrasonic_Sensor(trigger=19, echo=26)

try:

  while True:
    d = ultrasonic_sensor.get_distance()
    time.sleep(1)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()
