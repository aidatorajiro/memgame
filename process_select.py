# -*- coding: utf-8 -*-

from functools import partial
from memorpy import MemWorker, Process
from kivy.properties import ReferenceListProperty, ListProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation
from kivy.clock import Clock
from utils import draw_text_on_canvas

class ProcessSelect(Widget):
    current_process_index = NumericProperty(-1)
    time_left = NumericProperty(1) # time left until the character dives
    process_list = ListProperty([])

    overwrap = ObjectProperty(None)
    overwrap_pos_x = NumericProperty(0)
    overwrap_pos_y = NumericProperty(0)
    overwrap_pos = ReferenceListProperty(overwrap_pos_x, overwrap_pos_y)
    overwrap_size_w = NumericProperty(0)
    overwrap_size_h = NumericProperty(66)
    overwrap_size = ReferenceListProperty(overwrap_size_w, overwrap_size_h)
    overwrap_r = NumericProperty(1)
    overwrap_g = NumericProperty(1)
    overwrap_b = NumericProperty(1)
    overwrap_color = ReferenceListProperty(overwrap_r, overwrap_g, overwrap_b)
    overwrap_color_anim = ObjectProperty(None)

    text = ObjectProperty(None)
    text_pos_x = NumericProperty(0)
    text_pos_y = NumericProperty(0)
    text_pos = ReferenceListProperty(text_pos_x, text_pos_y)
    text_content = StringProperty("")

    dive_clock = ObjectProperty(None)
    finished = BooleanProperty(False)

    columns = 20
    cell_interval = 120
    cell_size = (64, 64)

    def start(self):
        """Initialize function."""
        try:
            self.process_list = Process.list()
            self.process_list.reverse()
        except:
            message("エラーが発生しました。管理者権限でこのゲームを実行してみてください。")
            return

        with self.canvas:
            i = 0

            for proc in self.process_list:
                # calculate position
                posx = (i % self.columns)*self.cell_interval
                posy = int(i / self.columns)*self.cell_interval

                # draw squares
                Color(1, 1, 1)
                Rectangle(pos=(posx, posy), size=self.cell_size)

                # draw text
                Color(0, 0, 0)
                draw_text_on_canvas(str(proc["pid"]), pos=(posx, posy))

                i += 1

    def update(self, _, chara):
        """Frame update function.
        Args:
            chara: character object"""

        coord = chara.coordinate

        if self.finished is True:
            return

        # calculate the index of selected process
        i = int(coord[0] / self.cell_interval) + int(coord[1] / self.cell_interval) * 20
        if (coord[0] < 0 or
                coord[1] < 0 or
                coord[0] > self.columns*self.cell_interval or
                coord[0] % self.cell_interval > self.cell_size[0] or
                coord[1] % self.cell_interval > self.cell_size[1] or
                i >= len(self.process_list)):
            i = -1 # case of no select or invalid select

        # if selected process changed
        if i != self.current_process_index:
            self.time_left = 1
            self.current_process_index = i

            # progress rectangle
            if i != -1:
                pid = self.process_list[i]["pid"]

                self.overwrap_color_anim = Animation(
                    overwrap_r=0.97,
                    overwrap_g=0.2,
                    overwrap_b=0,
                    overwrap_size_w=66,
                    duration=2.)

                self.dive_clock = Clock.schedule_once(partial(self.dive, pid), 2.)

                self.overwrap_color_anim.start(self)

                posx = (i % self.columns)*self.cell_interval
                posy = int(i / self.columns)*self.cell_interval

                self.overwrap_pos_x = posx-1
                self.overwrap_pos_y = posy-1

                self.text_content = str(pid)
                self.text_pos_x = posx
                self.text_pos_y = posy
            else:
                self.overwrap_r = 1
                self.overwrap_g = 1
                self.overwrap_b = 1
                self.overwrap_size_w = 0

                self.overwrap_color_anim.stop(self)

                self.dive_clock.cancel()
        else:
            self.time_left -= 0.01

        # draw progress rectangle
        if self.overwrap is not None:
            self.canvas.remove(self.overwrap)
            self.canvas.remove(self.text)

        with self.canvas:
            Color(*self.overwrap_color)
            self.overwrap = Rectangle(pos=self.overwrap_pos, size=self.overwrap_size)
            Color(0, 0, 0)
            self.text = draw_text_on_canvas(self.text_content, pos=self.text_pos)

    def dive(self, pid, _):
        """Diving function."""
        try:
            mw = MemWorker(pid=pid)
            self.finished = True
            anim = Animation(opacity = 0)
            anim.start(self)
        except:
            pass
