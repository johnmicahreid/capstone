import time
import RPi.GPIO as GPIO

# Define the pin we will be using 
led_pin = 21 

GPIO.setmode(GPIO.BCM) # BCM is a numbering system for the pins
GPIO.setup(led_pin, GPIO.OUT) # Set up pin 21 for output

led_pwm = GPIO.PWM(led_pin, 50)  # Pulse Width Modulation at 50Hz
led_pwm.start(0) # Start with the LED off

try:
	while (True):
		for brightness in range (0, 100, 5):
			led_pwm.ChangeDutyCycle(brightness)
			time.sleep(0.1) 

except KeyboardInterrupt: # clean up
	led_pwm.ChangeDutyCycle(0)
	led_pwm.stop()
	GPIO.cleanup()

