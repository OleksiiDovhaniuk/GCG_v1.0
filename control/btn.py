from kivy.lang import Builder
from control.hoverBehaviour import HoverButton


Builder.load_file('view/btn.kv')

class Btn(HoverButton):
    pass

class SaveAsBtn(Btn):
    pass

class OpenBtn(Btn):
    pass

class MinimiseBtn(Btn):
    pass

class MenuBarBtn(Btn):
    pass