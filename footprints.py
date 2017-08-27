from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Translate
from kivy.properties import ObjectProperty
from kivy.vector import Vector

class Footprints(Widget):
    """Footprints class."""
    colors = ObjectProperty({})

    def update(self, coord):
        """Frame update function. Draw registered footprints.

        Args:
            coord: the coordinate of the character"""

        self.colors[(coord[0], coord[1])] = 1

        self.canvas.clear()

        with self.canvas:
            Translate(self.pos[0], self.pos[1])
            for pos, c in self.colors.items():
                Color(c, c, c)
                Rectangle(pos=(pos[0] + 1, pos[1] + 1), size=(2, 2))
                self.colors[pos] *= 0.95
        
        for i in self.colors.keys():
            if self.colors[i] < 0.01:
                del self.colors[i]