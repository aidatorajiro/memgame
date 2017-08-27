from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Translate
from kivy.properties import ObjectProperty
from kivy.vector import Vector

class Footprints(Widget):
    """Footprints class."""
    colors = ObjectProperty({})

    def add_footprint(self, pos):
        """Register a footprint.

        Args:
            pos: tuple of two numbers
        """
        self.colors[pos] = 1

    def update(self):
        """Frame update function. Draw registered footprints."""
        self.canvas.clear()

        with self.canvas:
            Translate(self.pos[0], self.pos[1])
            for pos, c in self.colors.items():
                Color(c, c, c)
                Rectangle(pos=(pos[0] + 1, pos[1] + 1), size=(15, 15))
                self.colors[pos] *= 0.95