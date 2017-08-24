from kivy.app import App
from kivy.clock import Clock
from game import MemGame

class MemApp(App):
    def build(self):
        game = MemGame()
        game.start()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game