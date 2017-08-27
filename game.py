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

        # process select
        self.select.start()

    def update(self, _):
        """Frame update function."""

        # character
        self.chara.update()

        # footprint
        x = self.chara.coordinate[0]
        y = self.chara.coordinate[1]

        self.footprints.add_footprint((x - x % 16, y - y % 16))

        self.footprints.update()

        # update the position of the game objects
        obj_pos = Vector(*self.chara.pos) - self.chara.coordinate
        self.select.pos = self.footprints.pos = obj_pos
