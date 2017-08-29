from message_box import MessageBox
from character import Character
from translate_hack import TranslateHack
from footprints import Footprints
from process_select import ProcessSelect
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget

class MemGame(Widget):
    # game objects
    message_box = ObjectProperty(None)
    chara = ObjectProperty(None)
    select = ObjectProperty(None)
    footprints = ObjectProperty(None)

    def start(self):
        """Game initialize function."""

        # prepare process select
        self.select.start()

    def update(self, dt):
        """Frame update function."""

        # character
        self.chara.update(dt)

        # footprint
        self.footprints.update(dt, self.chara)

        # process select
        self.select.update(dt, self.chara)
