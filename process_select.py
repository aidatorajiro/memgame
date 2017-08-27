from memorpy import MemWorker
from memorpy import Process
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class ProcessSelect(Widget):
    # game objects
    process_list = ListProperty([])

    def start(self):
        """Initialize function."""
        self.process_list = Process.list()