# Copyright (C) 2017 Torajiro Aida
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from app import MemApp
from kivy.config import Config

if __name__ == '__main__':
    Config.set("input", "mouse", "mouse,disable_multitouch")
    Config.set("graphics", "multisamples", "0")
    MemApp().run()

import threading
import os
import signal

def hello():
    os.kill(os.getpid(), signal.SIGTERM)

t=threading.Timer(10,hello)
t.start()