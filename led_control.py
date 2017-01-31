import time
import RPi.GPIO as GPIO

class LED(object):

	def __init__(self, led_pin, brightness=50):
		self.led_pin = led_pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(led_pin, GPIO.OUT)

		self.led_pwm = GPIO.PWM(self.led_pin, 50)  # frequency=50Hz
		self.led_pwm.start(brightness)

	def set_brightness(self, brightness):
		self.led_pwm.ChangeDutyCycle(brightness)


	def stop(self):
		self.led_pwm.stop()

