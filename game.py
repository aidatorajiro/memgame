from kivy.properties import ObjectProperty
from character import Character
from kivy.uix.widget import Widget

class MemGame(Widget):
    chara = ObjectProperty(None)
    
    def start(self):
        self.chara.center = self.center
        self.chara.velocity = (0, 0)
    
    def update(self, dt):
        self.chara.move()
        pass