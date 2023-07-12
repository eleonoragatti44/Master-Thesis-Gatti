from vec2D import *
from individual import *
from parameters import *
from math import sqrt, pi
from numpy import random as rnd
import unittest

class TestVec2D(unittest.TestCase):
    def test_add(self):
        assert( (Vec2D(1.5, 0.5) + Vec2D(2.0, -0.5)).are_close(Vec2D(3.5, 0.)) )
    def test_sub(self):
        assert( (Vec2D(1.5, 0.5) - Vec2D(2.0, -0.5)).are_close(Vec2D(-0.5, 1)) )
        assert( (Vec2D(1.5, 0.5) - Vec2D(2.0, -0.5)).are_close(Vec2D(-0.5, 1)) )
    def test_neg(self):
        assert( (-Vec2D(1.5, 0.5)).are_close(Vec2D(-1.5, -0.5)) )
    def test_mul(self):
        assert( (Vec2D(1.5, 0.5)*2).are_close(Vec2D(3., 1.)) )
        assert( (Vec2D(1.5, 0.5) * Vec2D(2.0, -0.5)).are_close(Vec2D(3.0, -0.25)) )
    def test_div(self):
        assert( (Vec2D(1.5, 0.5)/2).are_close(Vec2D(0.75, 0.25)) )
        assert( (Vec2D(2.0, 5.0) / Vec2D(2.0, -0.5)).are_close(Vec2D(1.0, -10.0)) )
    def test_normalise(self):
        x : Vec2D
        assert( Vec2D(2, 0).normalise().are_close(Vec2D(1, 0)) )
        assert( Vec2D(1.5, 5).normalise().are_close((Vec2D(15, 50)*20).normalise()) )
        for i in range(100):
            x = Vec2D(1.0, 0.0).rotate(rnd.uniform() * 360.0)
            norm = x.normalise()
    def test_rotate(self):
        assert( (Vec2D(1, 0).rotate(math.radians(45))).are_close(Vec2D(sqrt(2)/2, sqrt(2)/2)) )
    def test_dot(self):
        assert( Vec2D(3, 1).dot(Vec2D(2, -4)) - 2 < 1e-5 )
        assert( Vec2D(-0.3, -0.5).dot(Vec2D(1, 2)) - (-1.3) < 1e-5 )
    def test_cross(self):
        assert( Vec2D(3, 1).cross(Vec2D(2, -4)) - (-14) < 1e-5 )
        assert( Vec2D(-0.3, -0.5).cross(Vec2D(1, 2)) - (-0.1) < 1e-5 )
    def test_distanceTo(self):
        assert( (Vec2D(0.5, 0.5)).distanceTo(Vec2D(-0.5, 0.5)) == 1 )
    def test_polarAngle(self):
        assert( (Vec2D(0.5, sqrt(3)/2).polarAngle() - math.radians(60)) < 1e-5 )
        assert( abs(Vec2D(-0.5, -sqrt(3)/2).polarAngle() - math.radians(-120)) < 1e-5 )
    def test_smallestAngleTo(self):
        assert( (Vec2D(0.5, sqrt(3)/2).smallestAngleTo(Vec2D(sqrt(3)/2, 0.5)) - 30) < 1e-5 )
        assert( (Vec2D(0.5, sqrt(3)/2).smallestAngleTo(Vec2D(-1, 0)) - 120) < 1e-5 )
        assert( (Vec2D(0.5, 0.5).smallestAngleTo(Vec2D(0, -1)) - 135) < 1e-5 )
    # def test_accuracy(self):
    #     assert( (Vec2D(1, 3)/2) == (Vec2D(1, 3)*0.5) )

    # def test_round(self):
    #     a = Vec2D(0.5, sqrt(3)/2)
    #     print(a.x, a.y)
    #     a.round()
    #     print(a.x, a.y)


class TestIndividual(unittest.TestCase):
    def test_MoveMyself(self):
        ind = Individual()
        ind.Setup(r_centre = Vec2D(0.5, 0.5), direction = Vec2D(1.0, 0.0), max_turning_rate = max_turning_rate, speed = speed,
                       zone_of_deflection = zod, zone_of_perception = zop, angular_error_sd = angular_error_sd, omega = set_omega, informed = 0)
        ind.Move(0.1, 0)
        assert( ind.r_centre.are_close(Vec2D(0.6, 0.5)) )

        ind.Setup(r_centre = Vec2D(0, 0), direction = Vec2D(1.0, 0.0), max_turning_rate = max_turning_rate, speed = speed,
                       zone_of_deflection = zod, zone_of_perception = zop, angular_error_sd = angular_error_sd, omega = set_omega, informed = 0)
        ind.desired_direction = Vec2D(0.5, 0.5).normalise()
        ind.Move(0.1, 0)
        if max_turning_rate*0.1 >= pi/4:
            assert( ind.r_centre.are_close(Vec2D(0.1*sqrt(2)/2, 0.1*sqrt(2)/2)) )
        '''
        else:
            print(ind.r_centre.x, ind.r_centre.y)
            assert( ind.r_centre.are_close(Vec2D(0.1, 0)) )
        '''
        '''
        GREAT! MOVE AND MOVEMYSELF WORK WELL!
        '''
    def test_AddPersonalPreference(delf):
        ind = Individual()
        ind.Setup(r_centre = Vec2D(0, 0), direction = Vec2D(1.0, 0.0), max_turning_rate = max_turning_rate, speed = speed,
                       zone_of_deflection = zod, zone_of_perception = zop, angular_error_sd = angular_error_sd, omega = set_omega, informed = 0)
        print(ind.desired_direction.x, ind.desired_direction.y)
        ind.AddPersonalPreference(Vec2D(5,5))
        print(ind.desired_direction.x, ind.desired_direction.y)
        # ??? How to test this?


if __name__ == "__main__":
    unittest.main()