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

from kivy.uix.widget import Widget
from memorpy import MemWorker
from kivy.properties import ObjectProperty
import random
import math
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from functools import partial
import threading
import time

class ProcessView(Widget):
    pid = None
    worker = None
    region = None

    chara = ObjectProperty(None)

    worldmap = {}

    world_width = None
    world_height = None
    update_width = 20
    update_height = 20

    stop_infinite_update_map = False

    def infinite_update_map(self):
        while not self.stop_infinite_update_map:
            self.update_map()
            time.sleep(1)

    def start(self, pid):
        self.pid = pid
        self.worker = MemWorker(pid=self.pid)
        self.region = random.choice(list(self.worker.process.iter_region()))
        self.world_width = self.world_height = int(math.sqrt(self.region[1]))
        Clock.schedule_interval(self.draw_map, 1 / 60)
        threading.Thread(target=self.infinite_update_map).start()
        print(self.region)

    def stop(self):
        self.stop_infinite_update_map = True

    def update_map(self):
        center = (int(self.chara.coordinate[0]) >> 4,
                  int(self.chara.coordinate[1]) >> 4)

        offset_x = self.world_width / 2
        offset_y = self.world_height / 2

        for i in range(int(self.chara.coordinate[0] - self.chara.pos[0]) >> 4,
                       int(self.chara.coordinate[0] + self.chara.pos[0]) >> 4):
            for j in range(int(self.chara.coordinate[1] - self.chara.pos[1]) >> 4,
                           int(self.chara.coordinate[1] + self.chara.pos[1]) >> 4):
                x = center[0] + i
                y = center[1] + j
                addr_x = x + offset_x
                addr_y = y + offset_y
                addr_x_mod = addr_x % self.world_width
                addr_y_mod = addr_y % self.world_height
                address = (self.region[0] +
                           self.world_width * addr_y_mod +
                           addr_x_mod)

                try:
                    b = ord(self.worker.process.read_bytes(address, bytes=1))
                except:
                    b = 0

                if b != 0:
                    self.worldmap[(x, y)] = b

    def draw_map(self, dt):
        self.canvas.clear()
        with self.canvas:
            for i in range(int(self.chara.coordinate[0] - self.chara.pos[0]) >> 4,
                           int(self.chara.coordinate[0] + self.chara.pos[0]) >> 4):
                for j in range(int(self.chara.coordinate[1] - self.chara.pos[1]) >> 4,
                               int(self.chara.coordinate[1] + self.chara.pos[1]) >> 4):
                    if (i, j) not in self.worldmap:
                        continue
                    c = float(self.worldmap[(i, j)]) / 255
                    Color(c, c, c)
                    Rectangle(pos=(i * 16 + 1, j * 16 + 1), size=(14, 14))
