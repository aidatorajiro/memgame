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

        x = coord[0]
        y = coord[1]
        
        self.colors[(x - x % 16, y - y % 16)] = 1

        self.canvas.clear()

        with self.canvas:
            Translate(self.pos[0], self.pos[1])
            for pos, c in self.colors.items():
                Color(c, c, c)
                Rectangle(pos=(pos[0] + 1, pos[1] + 1), size=(15, 15))
                self.colors[pos] *= 0.95