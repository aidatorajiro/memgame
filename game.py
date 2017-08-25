from character import Character
from process_select import ProcessSelect
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class MemGame(Widget):
    # game objects
    chara = ObjectProperty(None)
    select = ObjectProperty(None)

    def start(self):
        """Game initialize function."""
        self.chara.center = self.center
        self.chara.velocity = (0, 0)
        self.chara.coordinate = (0, 0)

        self.select.start()
        print(self.select.process_list)

    def update(self, _):
        """Frame update function."""

        def move_against_chara(obj):
            """Update the position of the given object against the character."""
            obj.pos = Vector(*obj.pos) - self.chara.velocity

        self.chara.update()
        move_against_chara(self.select)
