from app import MemApp
from kivy.config import Config

if __name__ == '__main__':
    Config.set("input", "mouse", "mouse,disable_multitouch")
    MemApp().run()