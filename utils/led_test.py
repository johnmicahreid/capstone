
import led_control
import time

led = led_control.LED(led_pin = 21, brightness = 80)

time.sleep(5)

led.stop()
