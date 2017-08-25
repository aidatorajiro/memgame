from character import Character
from footprints import Footprints
from process_select import ProcessSelect
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class MemGame(Widget):
    # game objects
    chara = ObjectProperty(None)
    select = ObjectProperty(None)
    footprints = ObjectProperty(None)

    def start(self):
        """Game initialize function."""
        self.chara.center = self.center
        self.chara.pos = (0, 0)
        self.chara.velocity = (0, 0)
        self.chara.coordinate = (0, 0)

        self.footprints.center = self.center

        self.select.start()

    def update(self, _):
        """Frame update function."""

        def move_against_chara(obj):
            """Update the position of the given object against the character."""
            obj.pos = Vector(*obj.pos) - self.chara.velocity

        # character
        self.chara.update()

        # footprint
        self.footprints.add_footprint(self.chara.coordinate)

        # other objects
        move_against_chara(self.select)
        move_against_chara(self.footprints)