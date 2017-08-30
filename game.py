from message_box import MessageBox
from character import Character
from translate_hack import TranslateHack
from footprints import Footprints
from process_select import ProcessSelect
from process_view import ProcessView
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget

class MemGame(Widget):
    # game objects
    message_box = ObjectProperty(None)
    chara = ObjectProperty(None)
    select = ObjectProperty(None)
    footprints = ObjectProperty(None)
    processview = ObjectProperty(None)

    def start(self):
        """Game initialize function."""

        # prepare process select
        self.select.start()
        self.select.bind(finished=self.after_select)

    def after_select(self, select, finished):
        self.processview.start(select.pid)

    def update(self, dt):
        """Frame update function."""

        # character
        self.chara.update(dt)

        # footprint
        self.footprints.update(dt, self.chara)

        # process select
        self.select.update(dt, self.chara)
