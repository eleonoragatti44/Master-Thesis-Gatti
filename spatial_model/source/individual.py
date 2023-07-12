from vec2D import Vec2D
from sys import float_info
import numpy
from parameters import *

EPSILON = float_info.epsilon

class Individual:
    """A class representing an individual."""
    r_centre : Vec2D = Vec2D()              # Rotational centre of the agent (cm)
    direction : Vec2D = Vec2D()             # Vector representing the current direction of the agent
    desired_direction : Vec2D = Vec2D()     # Vector representing the desired direction of the agent
    speed : float = 0.0                     # cm per second
    max_turning_rate : float = 0.0          # Maximum turning rate (degrees per second)
    zone_of_deflection : float = 0.0
    zone_of_perception : float = 0.0
    angular_error_sd : float = 0.0
    omega : float = 0.0
    zop_count : int = 0
    zod_count : int = 0
    equivalence_class : int = 0
    total_zod : Vec2D = Vec2D()
    total_zop : Vec2D = Vec2D()
    total_allignament : Vec2D = Vec2D()
    informed : int = 0                      # Index to enumerate each subgroup of informed individuals
    attraction : bool = False

    def Setup(self, r_centre, direction, max_turning_rate, speed, zone_of_deflection, zone_of_perception, angular_error_sd, omega, informed):
        """Setup individuals."""
        self.r_centre = r_centre
        self.direction = direction
        self.max_turning_rate = max_turning_rate
        self.speed = speed
        self.zone_of_deflection = zone_of_deflection
        self.zone_of_perception = zone_of_perception
        self.angular_error_sd = angular_error_sd
        self.omega = omega
        self.informed = informed

    def MoveMyself(self, timestep_inc):
        """Move the individual along the current direction."""
        self.r_centre += self.direction * self.speed * timestep_inc

    def TurnTowardsVector(self, vector, timestep_inc, dev_angle):
        """Turn direction towards a certain direction (vector).
        There is a threshold beyond which the direction is changed by a maximum angle
        dev_angle in radiant."""
        max_degrees : float = self.max_turning_rate * timestep_inc
        vector.rotate(dev_angle)
        check_angle : float = self.direction.smallestAngleTo(vector)
        if (check_angle <= max_degrees):
            self.direction = vector
        elif (check_angle > max_degrees):
            cross_product = self.direction.cross(vector)
            if (cross_product > 0):
                self.direction.rotate(max_degrees)
            else:
                self.direction.rotate(-max_degrees)

    def Move(self, timestep_inc, dev_angle, epsilon = 1e-10):
        """Move the individual along the desired direction if not zero."""
        if(abs(self.desired_direction.x) < epsilon and abs(self.desired_direction.y) < epsilon):
            self.TurnTowardsVector(self.direction, timestep_inc, dev_angle)
        else:
            self.TurnTowardsVector(self.desired_direction, timestep_inc, dev_angle)
        self.MoveMyself(timestep_inc)

    def AddPersonalPreference(self, cue_centre):
        """Add personal preference to the direction, tuned by omega parameter."""
        goal : Vec2D = (cue_centre - self.r_centre).normalise()
        goal *= self.omega
        self.desired_direction += goal
        self.desired_direction.normalise()
        
    def Feedback(self, cue_centre, angular_thresh, omega_inc, omega_dec, omega_max):
        """Add feedback to the direction."""
        temp_vec : Vec2D = (cue_centre - self.r_centre).normalise()
        if positive_feedback == True:
            if (self.direction.smallestAngleTo(temp_vec) < angular_thresh):
                self.omega += omega_inc
                self.omega = self.omega
                if (self.omega > omega_max):
                    self.omega = omega_max
            else:
                self.omega -= omega_dec
                if (self.omega < 0):
                    self.omega = 0
        else:
            if (self.direction.smallestAngleTo(temp_vec) > angular_thresh):
                self.omega -= omega_dec
                if (self.omega < 0):
                    #print('min')
                    self.omega = 0

agent = [Individual() for i in range(total_agents)]
'''
def Copy(self, other):
    self.r_centre = other.r_centre
    self.direction = other.direction
    self.max_turning_rate = other.max_turning_rate
    self.speed = other.speed
    self.zone_of_deflection = other.zone_of_deflection
    self.zone_of_perception = other.zone_of_perception
    self.angular_error_sd = other.angular_error_sd
'''