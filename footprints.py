from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import ObjectProperty
from kivy.vector import Vector

class Footprints(Widget):
    group = ObjectProperty(None)

    def add_footprint(self, pos):
        """Draw a footprint."""
        with self.canvas:
            color = Color(1, 1, 1)
            Rectangle(pos=pos, size=(1, 1))