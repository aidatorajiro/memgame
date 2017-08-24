from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty
from kivy.vector import Vector
import math
import random

class Character(Widget):
    vx = NumericProperty(0)
    vy = NumericProperty(0)
    velocity = ReferenceListProperty(vx, vy)
    
    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)
    a = NumericProperty(1)
    color = ReferenceListProperty(r, g, b, a)
    
    def vel_magnitude(self):
        return self.velocity[0] ** 2 + self.velocity[1] ** 2
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        self.vx *= 0.995
        self.vy *= 0.995
        
        # blinking
        rand = random.random()
        if rand < 0.06 - math.atan(self.vel_magnitude()) / math.pi / 10:
            self.color = (0, 0, 0, 0)
        else:
            self.color = (1, 1, 1, 1)
    
    def on_touch_down(self, touch):
        self.vx += math.atan(touch.pos[0] - self.pos[0])
        self.vy += math.atan(touch.pos[1] - self.pos[1])