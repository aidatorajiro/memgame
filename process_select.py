from memorpy import MemWorker, Process
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class ProcessSelect(Widget):
    # game objects
    process_list = ListProperty([])

    def start(self):
        """Initialize function."""
        self.process_list = Process.list()
        with self.canvas:
            i = 0
            for proc in self.process_list:
                Color(1, 1, 1)
                Rectangle(pos=(i*80, 0), size=(64, 64))
                i += 1

    def update(self, coord):
        """Frame update function."""
