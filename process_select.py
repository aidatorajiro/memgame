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

    rect = ObjectProperty(None)
    rect_pos_x = NumericProperty(0)
    rect_pos_y = NumericProperty(0)
    rect_pos = ReferenceListProperty(rect_pos_x, rect_pos_y)
    rect_r = NumericProperty(1)
    rect_g = NumericProperty(1)
    rect_b = NumericProperty(1)
    rect_color = ReferenceListProperty(rect_r, rect_g, rect_b)
    rect_color_anim = ObjectProperty(None)

    text = ObjectProperty(None)
    text_pos_x = NumericProperty(0)
    text_pos_y = NumericProperty(0)
    text_pos = ReferenceListProperty(text_pos_x, text_pos_y)
    text_content = StringProperty("")

    dive_clock = ObjectProperty(None)
    dive_phase = BooleanProperty(False)

    columns = 20
    rect_interval = 120
    rect_size = 64

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
                posx = (i % self.columns)*self.rect_interval
                posy = int(i / self.columns)*self.rect_interval

                # draw squares
                Color(1, 1, 1)
                Rectangle(pos=(posx, posy), size=(self.rect_size, self.rect_size))

                # draw text
                Color(0, 0, 0)
                draw_text_on_canvas(str(proc["pid"]), pos=(posx, posy))

                i += 1

    def update(self, coord):
        """Frame update function."""

        if self.dive_phase is True:
            return

        # calculate the index of selected process
        i = int(coord[0] / self.rect_interval) + int(coord[1] / self.rect_interval) * 20
        if (coord[0] < 0 or
                coord[1] < 0 or
                coord[0] > self.columns*self.rect_interval or
                coord[0] % self.rect_interval > self.rect_size or
                coord[1] % self.rect_interval > self.rect_size or
                i >= len(self.process_list)):
            i = -1 # case of no select or invalid select

        # if selected process changed
        if i != self.current_process_index:
            self.time_left = 1
            self.current_process_index = i

            # progress rectangle
            if i != -1:
                pid = self.process_list[i]["pid"]

                self.rect_color_anim = Animation(
                    rect_r=0.97,
                    rect_g=0.2,
                    rect_b=0,
                    duration=2.)

                self.dive_clock = Clock.schedule_once(partial(self.dive, pid), 2.)

                self.rect_color_anim.start(self)

                posx = (i % self.columns)*self.rect_interval
                posy = int(i / self.columns)*self.rect_interval

                self.rect_pos_x = posx-1
                self.rect_pos_y = posy-1

                self.text_content = str(pid)
                self.text_pos_x = posx
                self.text_pos_y = posy
            else:
                self.rect_r = 1
                self.rect_g = 1
                self.rect_b = 1

                self.rect_color_anim.stop(self)

                self.dive_clock.cancel()
        else:
            self.time_left -= 0.01

        # draw progress rectangle
        if self.rect is not None:
            self.canvas.remove(self.rect)
            self.canvas.remove(self.text)

        with self.canvas:
            Color(*self.rect_color)
            self.rect = Rectangle(pos=self.rect_pos, size=(66, 66))
            Color(0, 0, 0)
            self.text = draw_text_on_canvas(self.text_content, pos=self.text_pos)

    def dive(self, pid, _):
        """Diving function."""
        try:
            mw = MemWorker(pid=pid)
            self.dive_phase = True
            anim = Animation(opacity = 0)
            anim.start(self)
        except:
            pass
