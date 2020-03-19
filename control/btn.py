from kivy.lang import Builder
from kivy.factory import Factory

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

# Factory.register('Btn', cls=Btn)
# Factory.register('BtnSaveAs', cls=SaveAsBtn)
# Factory.register('BtnOpen', cls=OpenBtn)
# Factory.register('MinimiseBtn', cls=MinimiseBtn)
# Factory.register('MenuBarBtn', cls=MenuBarBtn)