from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import ultrasonic
import movement
import led_control
import car_detection
import lane_detection
import RPi.GPIO as GPIO
import cv2
import numpy


#GPIO.cleanup() # Reset the GPIO pins incase they were still in use

# GPIO pin numbers

# ultrasonic
trigger_pin = 19
echo_pin = 26

# motors 
motor_left_in1_pin=27
motor_left_in2_pin=22
motorpwm_left_in1_pin = 4
motor_right_in1_pin = 24
motor_right_in2_pin = 25
motorpwm_right_in1_pin = 18

# LED
led_pin = 21

# Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 16
rawCapture=PiRGBArray(camera, size=(640, 480))
camera.hflip = True
camera.vflip = True
time.sleep(0.1)

# Create the objects we will be using
ultra = ultrasonic.SRF05_Ultrasonic_Sensor(trigger=trigger_pin, echo=echo_pin)
motors = movement.Motors(maxspeed = 60)
led = led_control.LED(led_pin = led_pin, brightness = 80)
lane_tracker = lane_detection.LaneTracker()
#car_det = car_detection.CarDetector()

try:
    #motors.backward()
    #motors.start(60)
    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                               use_video_port=True):

        if ultra.get_distance_filtered() < 15:
            print("Proximity warning") 
            motors.stop()
            
        else:
            image=frame.array
##            ret = car_det.get_centre(image)
##            if ret is not None:
##                (centre, rad) = ret
##                car_det.show_img(centre, rad)
##                offset = car_det.get_offset(centre)
##                #print(offset)
##                motors.set_LR_speed(offset, (1.0/320.0))
##                print(motors.get_speeds())
##            else:
##                motors.stop() 
            lane_tracker.update_img(image)
            print(lane_tracker.get_mid_lane())
            lane_tracker.show_img()

        rawCapture.truncate(0)

except KeyboardInterrupt:
    pass

motors.stop()
led.stop()
#ultrasonic_sensor.stop()

GPIO.cleanup()
