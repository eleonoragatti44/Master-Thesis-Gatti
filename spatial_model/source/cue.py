from vec2D import Vec2D

class Cue:
    centre : Vec2D = Vec2D()
    def Setup(self, centre = Vec2D()):
        self.centre = centre