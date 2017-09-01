# -*- coding: utf-8 -*-

from functools import partial
from memorpy import MemWorker, Process
from kivy.properties import (ReferenceListProperty,
                             ListProperty,
                             NumericProperty,
                             ObjectProperty,
                             BooleanProperty,
                             StringProperty)
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import InstructionGroup
from kivy.animation import Animation
from kivy.clock import Clock
from utils import draw_text_on_canvas
import os

class ProcessSelect(Widget):
    pid = NumericProperty(-1)

    chara = ObjectProperty(None)

    current_process_index = NumericProperty(-1)
    process_list = []

    dive_clock = None
    finished = BooleanProperty(False)

    columns = 20
    cell_interval = 120
    cell_size = (64, 64)

    # instruction groups
    cells = None
    overwrap = None
    lebels = None

    # properties about overwrap rectangle
    overwrap_pos_x = NumericProperty(0)
    overwrap_pos_y = NumericProperty(0)
    overwrap_pos = ReferenceListProperty(overwrap_pos_x, overwrap_pos_y)
    overwrap_size_w = NumericProperty(0)
    overwrap_size_h = NumericProperty(62)
    overwrap_size = ReferenceListProperty(overwrap_size_w, overwrap_size_h)
    overwrap_r = NumericProperty(0.03)
    overwrap_g = NumericProperty(0.8)
    overwrap_b = NumericProperty(1)
    overwrap_a = NumericProperty(0)
    overwrap_color = ReferenceListProperty(overwrap_r, overwrap_g, overwrap_b, overwrap_a)
    overwrap_color_anim = None

    def index_to_pos(self, i):
        """Calculate position from index"""
        posx = (i % self.columns)*self.cell_interval
        posy = int(i / self.columns)*self.cell_interval
        return posx, posy

    def pos_to_index(self, pos):
        i = int(pos[0] / self.cell_interval) + int(pos[1] / self.cell_interval) * 20

        if (pos[0] < 0 or
                pos[1] < 0 or
                pos[0] > self.columns*self.cell_interval or
                pos[0] % self.cell_interval > self.cell_size[0] or
                pos[1] % self.cell_interval > self.cell_size[1] or
                i >= len(self.process_list)):
            i = -1 # case of no select or invalid select

        return i

    def start(self):
        """Initialize function."""
        try:
            self.process_list = Process.list()
            self.process_list.reverse()
        except:
            message("エラーが発生しました。管理者権限でこのゲームを実行してみてください。")
            return

        self.cells = InstructionGroup()
        self.overwrap = InstructionGroup()
        self.lebels = InstructionGroup()

        i = 0

        pid_of_this_program = os.getpid()

        for proc in self.process_list:
            # calculate position
            posx, posy = self.index_to_pos(i)

            # draw squares
            if proc["pid"] == pid_of_this_program:
                self.cells.add(Color(0.8, 0.8, 0.8))
            else:
                self.cells.add(Color(1, 1, 1))

            self.cells.add(Rectangle(pos=(posx, posy), size=self.cell_size))

            # draw text
            self.lebels.add(Color(0, 0, 0))
            self.lebels.add(draw_text_on_canvas(str(proc["pid"]), pos=(posx, posy)))

            i += 1
        
        self.canvas.add(self.cells)
        self.canvas.add(self.overwrap)
        self.canvas.add(self.lebels)

    def update(self, dt):
        """Frame update function."""

        coord = self.chara.coordinate

        if self.finished is True:
            return

        # calculate the index of selected process
        i = self.pos_to_index(coord)

        # if selected process changed
        if i != self.current_process_index:
            self.time_left = 1
            self.current_process_index = i

            # progress rectangle
            if i != -1:
                self.overwrap_color_anim = Animation(
                    overwrap_a=1,
                    overwrap_size_w=62,
                    duration=2.)

                self.dive_clock = Clock.schedule_once(partial(self.dive, i), 2.)

                self.overwrap_color_anim.start(self)

                posx, posy = self.index_to_pos(i)

                self.overwrap_pos_x = posx+1
                self.overwrap_pos_y = posy+1
            else:
                self.overwrap_a = 0
                self.overwrap_size_w = 0
                self.overwrap_color_anim.stop(self)
                self.dive_clock.cancel()

        # draw overwrap
        self.overwrap.clear()
        self.overwrap.add(Color(*self.overwrap_color))
        self.overwrap.add(Rectangle(pos=self.overwrap_pos, size=self.overwrap_size))

    def dive(self, index, _):
        """Diving function."""
        self.pid = self.process_list[index]["pid"]
        try:
            MemWorker(pid=self.pid)
        except:
            posx, posy = self.index_to_pos(index)
            with self.canvas:
                Color(0.97, 0.1, 0)
                draw_text_on_canvas("ERROR", font_size=20, pos=(posx+1, posy+30))
        else:
            self.finished = True
            anim = Animation(opacity=0)
            def tmp(*args):
                self.canvas.clear()
            anim.bind(on_complete=tmp)
            anim.start(self)
