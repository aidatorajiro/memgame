"""Character module."""

import math
import random
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty
from kivy.vector import Vector
from kivy.animation import Animation

class Character(Widget):
    """Character class."""

    # absolute position of the character
    cx = NumericProperty(0)
    cy = NumericProperty(0)
    coordinate = ReferenceListProperty(cx, cy)

    # velocity of the character
    vx = NumericProperty(0)
    vy = NumericProperty(0)
    velocity = ReferenceListProperty(vx, vy)

    # color of the character
    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)
    a = NumericProperty(1)
    color = ReferenceListProperty(r, g, b, a)

    def vel_magnitude(self):
        """Returns the magnitude of the velocity"""
        return self.velocity[0] ** 2 + self.velocity[1] ** 2

    def update(self):
        """Frame update function.
        It updates some internal parameters and character's appearance by following order:
        1. Update the character's coordinate by the velocity.
        2. Decrease the velocity.
        3. Blink the character at random.
        """

        # update coordinate
        self.coordinate = Vector(*self.velocity) + self.coordinate
        self.vx *= 0.995
        self.vy *= 0.995

        # blinking
        rand = random.random()
        if rand < 0.06 - math.atan(self.vel_magnitude()) / math.pi / 10:
            self.color = (0, 0, 0, 0)
        else:
            self.color = (1, 1, 1, 1)

    def on_touch_down(self, touch):
        """Touch down function.
        Increase the velocity.
        """

        anim = Animation(vx=self.vx + math.atan((touch.pos[0] - self.pos[0]) / 10) / math.pi, 
                         vy=self.vy + math.atan((touch.pos[1] - self.pos[1]) / 10) / math.pi)
        
        anim.start(self)
