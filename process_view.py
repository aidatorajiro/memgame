from kivy.uix.widget import Widget
from memorpy import MemWorker
import random

class ProcessView(Widget):
    pid = None
    worker = None
    worldmap = {}
    regions = None

    search_width = 128
    search_height = 128

    world_width = None
    world_height = None

    def get_bytes(self, start, length):
        return self.worker.process.read_bytes(start, length)

    def update_world(self, center):
        startpos = (center[0] - self.search_width / 2, center[0] - self.search_height / 2)
        offset = self.world_width * startpos[1] + startpos[0]
        for i in range(0, self.search_height):
            bs = self.get_bytes(offset + i * self.search_width, self.search_width)
            for j, b in enumerate(bs):
                self.worldmap[(j, i)] = b

    def start(self, pid):
        self.pid = pid
        self.worker = MemWorker(pid=self.pid)
        self.regions = list(self.worker.process.iter_region())
