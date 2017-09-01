from kivy.uix.widget import Widget
from memorpy import MemWorker
from kivy.properties import ObjectProperty
import random
import math
from kivy.graphics import Rectangle, Color

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

    def start(self, pid):
        self.pid = pid
        self.worker = MemWorker(pid=self.pid)
        self.region = random.choice(list(self.worker.process.iter_region()))
        self.world_width = self.world_height = int(math.sqrt(self.region[1]))

        print(self.region)

    def update_map(self):
        center = (int(self.chara.coordinate[0]) >> 4,
                  int(self.chara.coordinate[1]) >> 4)
        
        offset_x = self.world_width / 2
        offset_y = self.world_height / 2

        for i in range(-self.update_height / 2, self.update_height - self.update_height / 2):
            for j in range(-self.update_width / 2, self.update_width - self.update_width / 2):
                x = center[0] + j
                y = center[1] + i
                addr_x = x + offset_x
                addr_y = y + offset_y
                addr_x_mod = addr_x % self.world_width
                addr_y_mod = addr_y % self.world_width
                address = (self.region[0] +
                           self.world_width * addr_y_mod +
                           addr_x_mod)

                try:
                    b = ord(self.worker.process.read_bytes(address, bytes=1))
                except:
                    b = 0

                if b != 0:
                    self.worldmap[(x, y)] = b

    def draw_map(self):
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

    def update(self, dt):
        self.update_map()
        self.draw_map()