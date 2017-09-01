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