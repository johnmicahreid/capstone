import RPi.GPIO as GPIO
import ultrasonic
import time

ultra = ultrasonic.SRF05_Ultrasonic_Sensor(trigger = 19, echo = 26)

for i in range(100):
    print("Distance is %s" % ultra.get_distance_filtered())
    time.sleep(0.1)
