# -*- coding: utf-8 -*-

from memorpy import MemWorker, Process
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Rectangle, Color

class ProcessSelect(Widget):
    # game objects
    process_list = ListProperty([])
    columns = 20

    def start(self):
        """Initialize function."""
        try:
            self.process_list = Process.list()
        except:
            self.error("エラーが発生しました。管理者権限でこのゲームを実行してみてください。")
            return

        with self.canvas:
            i = 0

            for proc in self.process_list:
                # calculate position
                posx = (i % self.columns)*80
                posy = int(i / self.columns)*80

                # draw squares
                Color(1, 1, 1)
                Rectangle(pos=(posx, posy), size=(64, 64))

                # get text texture
                label = CoreLabel(text=str(proc["pid"]))
                label.refresh()
                tex   = label.texture

                # draw text
                Color(0, 0, 0)
                Rectangle(size=tex.size, pos=(posx, posy), texture=tex)

                i += 1

    def update(self, coord):
        """Frame update function."""
