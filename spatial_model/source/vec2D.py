import math
import cmath
from sys import float_info

class Vec2D:
    """A 2D vector.
    This class has two floating-point fields: `x` and `y`."""
    x : float = 0.0
    y : float = 0.0

    def are_close(self, other, epsilon=1e-5):
        """Return True if the object and 'other' are roughly the same.
        This is needed becouse of python approximations."""
        return abs(self.x - other.x) < epsilon and abs(self.y - other.y) < epsilon
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Sum two vectors"""
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract one vector from another"""
        return Vec2D(self.x - other.x, self.y - other.y)

    def __neg__(self):
        """Return the reversed vector"""
        return Vec2D(-self.x, -self.y)

    def __mul__(self, other):
        """Compute the product between two vectors - elementwise or between a vector and a scalar"""
        try:
            # Try a vector-times-vector operation
            return Vec2D(self.x * other.x, self.y * other.y)
        except AttributeError:
            # Fall back to a vector-times-scalar operation
            return Vec2D(self.x * other, self.y * other)

    def __truediv__(self, other):
        """Compute the division between two vectors - elementwise or between a vector and a scalar"""
        try:
            # Try a vector-div-vector operation
            return Vec2D(self.x / other.x, self.y / other.y)
        except AttributeError:
            # Fall back to a vector-div-scalar operation
            return Vec2D(self.x / other, self.y / other)
    
    def dot(self, other):
        """Compute the dot product between two vectors"""
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        """Compute the cross (outer) product between two vectors"""
        return self.x * other.y - self.y * other.x

    def squared_norm(self):
        """Return the squared norm (Euclidean length) of a vector"""
        return self.x ** 2 + self.y ** 2

    def norm(self):
        """Return the norm (Euclidean length) of a vector"""
        return math.sqrt(self.squared_norm())

    def normalise(self):
        """Modify the vector's norm so that it becomes equal to 1"""
        if self.norm() != 0:
            norm = self.norm()
            self.x /= norm
            self.y /= norm
        return self

    def rotate(self, angle):
        """Rotate a vector of a certain angle in radiants."""
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        self.x = x
        self.y = y
        return self

    def distanceTo(self, other):
        """Compute the distance between two vectors."""
        x = self.x - other.x
        y = self.y - other.y
        return x * x + y * y

    def polarAngle(self):
        """Compute the angle from x-axis (east) to vector - counterclockwise.
            The result is an angle in [-pi, pi]."""
        r, phi = cmath.polar(complex(self.x, self.y))
        return phi

    def smallestAngleTo(self, other):
        """Compute the smaller of the two angles between two vectors with the same origin in rad."""
        vec1 : Vec2D = self
        vec2 : Vec2D = other
        vec1.normalise()
        vec2.normalise()
        if vec1.norm()==0 or vec2.norm()==0:
            return 0
        else:
            angle = vec1.dot(vec2)/(vec1.norm()*vec2.norm())
            if angle > 1: angle = 1
            if angle < -1: angle = -1
            return (math.acos(angle))

    def clear(self):
        """Reset the fields to 0."""
        self.x = 0
        self.y = 0

    def round(self):
        """Round the coordinates of a Vec2D to the 8th digit."""
        self.x = round(self.x, 8)
        self.y = round(self.y, 8)