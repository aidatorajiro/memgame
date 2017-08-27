from character import Character
from translate_hack import TranslateHack
from footprints import Footprints
from process_select import ProcessSelect
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.graphics import Translate

class MemGame(Widget):
    # game objects
    chara = ObjectProperty(None)
    select = ObjectProperty(None)
    footprints = ObjectProperty(None)

    def start(self):
        """Game initialize function."""

        # prepare process select
        self.select.start()

    def update(self, _):
        """Frame update function."""

        # character
        self.chara.update()

        # footprint
        self.footprints.update(self.chara.coordinate)

        # process select
        self.select.update(self.chara.coordinate)