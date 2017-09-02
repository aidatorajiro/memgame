# Copyright (C) 2017 Torajiro Aida
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
    
    def stop(self):
        self.processview.stop() # to stop threading

    def after_select(self, select, finished):
        self.processview.start(select.pid)

    def update(self, dt):
        """Frame update function."""

        # character
        self.chara.update(dt)

        # footprint
        self.footprints.update(dt)

        # process select
        self.select.update(dt)