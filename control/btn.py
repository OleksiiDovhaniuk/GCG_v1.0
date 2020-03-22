from kivy.lang import Builder
from control.hoverBehaviour import HoverButton

from design import Design


Builder.load_file('view/btn.kv')

class Btn(HoverButton):
    theme = Design().default_theme

class SaveAsBtn(Btn):
    pass

class OpenBtn(Btn):
    pass

class ArrowBtn(Btn):
    pass