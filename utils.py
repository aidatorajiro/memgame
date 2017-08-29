from kivy.core.text import Label as CoreLabel
from kivy.graphics import Rectangle

def draw_text_on_canvas(arg_text, font_size=12, **kwargs):
    # get text texture
    label = CoreLabel(text=arg_text, font_size=font_size)
    label.refresh()
    tex = label.texture

    # draw text
    return Rectangle(size=tex.size, texture=tex, **kwargs)
