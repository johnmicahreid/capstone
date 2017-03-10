# A PID controller helps to control the motion of the car by continuously calculating an error value
# based on three terms (proportional, integral and derivating) 

import motors

class PIDController(object):
    def __init__(self, P, I, D, maxspeed, steering_angle):
        self.P = P
        self.I = I
        self.D = D
        self.maxspeed = maxspeed
        self.steering_angle = steering_angle
        
    def get_LR_speed(self, offset):
        offset = offset*self.steering_angle
        if (offset > 0):
            return (self.maxspeed * (1-offset), self.maxspeed)
        else:
            return (self.maxspeed, self.maxspeed * (1 + offset))

            