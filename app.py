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

from kivy.app import App
from kivy.clock import Clock
from game import MemGame

class MemApp(App):
    game = None

    def build(self):
        self.game = MemGame()
        self.game.start()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        return self.game

    def on_stop(self):
        self.game.stop()